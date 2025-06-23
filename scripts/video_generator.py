# scripts/video_generator.py

import os
import re
import numpy as np
import pygame
import moderngl
import requests
from openai import OpenAI
from moviepy.editor import ImageSequenceClip, AudioFileClip

import config

# ==== SETTINGS from config.py ====
WIDTH       = config.WIDTH
HEIGHT      = config.HEIGHT
FPS         = config.FPS
OUTPUT_DIR  = config.OUTPUT_DIR
SHADER_PATH = config.SHADER_PATH
VIDEO_PATH  = config.VIDEO_PATH

# ==== CLEAN GENERATED GLSL ====
def clean_ai_shader(code: str) -> str:
    code = re.sub(r"^```(?:glsl)?", "", code, flags=re.IGNORECASE | re.MULTILINE)
    code = code.replace("```", "")
    code = code.replace("fragCoord", "gl_FragCoord.xy")
    code = code.replace("gl_FragColor", "fragColor")

    lines = code.strip().splitlines()
    lines = [line.strip() for line in lines if line.strip() and not line.startswith("//")]

    if not lines[0].startswith("#version"):
        lines.insert(0, "#version 330 core")
    if any("fragColor" in line for line in lines) and not any("out vec4 fragColor;" in line for line in lines):
        lines.insert(1, "out vec4 fragColor;")
    return "\n".join(lines)

# ==== MAIN GENERATION FUNCTION ====
def generate_video(payload, max_retries=3):
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    music_url  = payload.get("music_url")
    audio_path = None
    duration   = 5

    # ==== Download & inspect audio ====
    if music_url:
        try:
            print(f"🎵 Downloading music from {music_url}...")
            r = requests.get(music_url)
            r.raise_for_status()
            os.makedirs("temp", exist_ok=True)
            audio_path = os.path.join("temp", "audio.mp3")
            with open(audio_path, "wb") as f:
                f.write(r.content)
            print("🎵 MP3 downloaded successfully.")

            audio_clip = AudioFileClip(audio_path)
            duration   = int(audio_clip.duration)
        except Exception as e:
            print(f"[WARNING] Failed to download or process audio: {e}")
            audio_path = None
            audio_clip = None

    total_frames = duration * FPS

    # ==== Generate & compile shader ====
    for attempt in range(max_retries):
        print(f"Attempting shader generation… (try {attempt+1}/{max_retries})")
        prompt = f"""
        You are a GLSL shader artist. Generate a creative and abstract fragment shader for a music visualizer.

        The shader must reflect these musical characteristics:
        - Mood: {', '.join(payload.get('moods', []))}
        - Genre: {', '.join(payload.get('genres', []))}
        - Theme: {', '.join(payload.get('themes', []))}

        Constraints:
        - GLSL version: `#version 330 core`
        - Use only: `iTime`, `iResolution`, `u_audioIntensity`
        - Declare: `out vec4 fragColor;`
        - Do NOT use: `noise()`, `texture2D()`, `gl_FragColor`
        - Do NOT use deprecated or undefined functions
        - No explanations. Return GLSL code only.
        """

        response    = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            max_tokens=800
        )
        raw_shader  = response.choices[0].message.content
        safe_shader = clean_ai_shader(raw_shader)

        os.makedirs("temp", exist_ok=True)
        with open(SHADER_PATH, "w") as f:
            f.write(safe_shader.strip())

        try:
            test_ctx = moderngl.create_standalone_context()
            test_ctx.program(
                vertex_shader="""
                    #version 330
                    in vec2 in_vert;
                    void main() { gl_Position = vec4(in_vert, 0.0, 1.0); }
                """,
                fragment_shader=safe_shader,
            )
            print("Shader compiled successfully.")
            break
        except moderngl.Error as e:
            print(f"Shader failed on attempt {attempt+1}:\n", e)
    else:
        raise RuntimeError("All shader generation attempts failed. Try again or adjust the prompt.")

    # ==== RENDER FRAMES ====
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)
    ctx = moderngl.create_context()

    with open(SHADER_PATH, "r") as file:
        fragment_shader = file.read()

    prog = ctx.program(
        vertex_shader="""
            #version 330
            in vec2 in_vert;
            void main() { gl_Position = vec4(in_vert, 0.0, 1.0); }
        """,
        fragment_shader=fragment_shader,
    )

    # Set iResolution if present
    if "iResolution" in prog:
        dim = prog["iResolution"].dimension
        prog["iResolution"].value = (
            (WIDTH, HEIGHT) if dim == 2 else (WIDTH, HEIGHT, 0.0)
        )

    print("Rendering frames…")
    vertices = np.array([[-1, -1], [1, -1], [-1, 1], [1, 1]], dtype='f4')
    vbo      = ctx.buffer(vertices.tobytes())
    vao      = ctx.simple_vertex_array(prog, vbo, 'in_vert')

    for i in range(total_frames):
        t = i / FPS
        if "iTime" in prog:
            prog['iTime'].value = t
        if "u_audioIntensity" in prog:
            prog['u_audioIntensity'].value = np.sin(t * 2.0) * 0.5 + 0.5

        ctx.clear()
        vao.render(moderngl.TRIANGLE_STRIP)
        data  = ctx.screen.read(components=3)
        frame = np.frombuffer(data, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))[::-1]
        frame_path = os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png")
        pygame.image.save(pygame.surfarray.make_surface(frame.swapaxes(0, 1)), frame_path)
        print(f"Frame {i+1}/{total_frames}")

    pygame.quit()
    print("🎬 Encoding video…")

    clip = ImageSequenceClip(OUTPUT_DIR, fps=FPS)
    if audio_path:
        audio_clip = AudioFileClip(audio_path).set_duration(duration)
        clip = clip.set_audio(audio_clip)

    clip.write_videofile(VIDEO_PATH, codec="libx264", audio_codec="aac")
    print(f"✅ Video saved to: {VIDEO_PATH}")
    return VIDEO_PATH
