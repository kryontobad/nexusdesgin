"""
A modern, eye-catching "Nga, you made it!" window using pywebview.
Just run: python script.py
Requirements: pip install pywebview
"""

import webview

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>You made it!</title>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        width: 100vw;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        overflow: hidden;
        position: relative;
    }

    /* Confetti canvas placed behind the card */
    #confetti-canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }

    .card {
        position: relative;
        z-index: 10;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.3);
        padding: 3rem 4rem;
        text-align: center;
        animation: cardPop 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) both;
    }

    @keyframes cardPop {
        0% {
            transform: scale(0.5);
            opacity: 0;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }

    .title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(to right, #f12711, #f5af19);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from {
            filter: drop-shadow(0 0 5px rgba(245, 175, 25, 0.5));
        }
        to {
            filter: drop-shadow(0 0 25px rgba(245, 175, 25, 0.9));
        }
    }

    .subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }

    .close-btn {
        background: linear-gradient(135deg, #f12711, #f5af19);
        border: none;
        padding: 0.9rem 2.5rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        color: white;
        cursor: pointer;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }

    .close-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        filter: brightness(1.1);
    }

    .close-btn:active {
        transform: translateY(0);
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
    }

    /* Glowing dots decoration (top right / bottom left) */
    .decor {
        position: absolute;
        width: 250px;
        height: 250px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(245,175,25,0.15) 0%, transparent 70%);
        z-index: 0;
    }
    .decor.top {
        top: -70px;
        right: -70px;
    }
    .decor.bottom {
        bottom: -70px;
        left: -70px;
        background: radial-gradient(circle, rgba(241,39,17,0.15) 0%, transparent 70%);
    }
</style>
</head>
<body>

    <!-- Decorative glowing blobs -->
    <div class="decor top"></div>
    <div class="decor bottom"></div>

    <!-- Confetti canvas -->
    <canvas id="confetti-canvas"></canvas>

    <!-- Main card -->
    <div class="card">
        <h1 class="title">Nga, you made it!</h1>
        <p class="subtitle">Congratulations! Your hard work paid off 🎉</p>
        <button class="close-btn" onclick="dismiss()">Let's Go!</button>
    </div>

<script>
    // ===================== CONFETTI ANIMATION =====================
    (function() {
        const canvas = document.getElementById('confetti-canvas');
        const ctx = canvas.getContext('2d');
        let width, height;
        let particles = [];
        const colors = ['#f12711', '#f5af19', '#ffeb3b', '#ff5722', '#e91e63', '#9c27b0', '#00bcd4', '#4caf50'];

        function resize() {
            width = window.innerWidth;
            height = window.innerHeight;
            canvas.width = width;
            canvas.height = height;
        }
        window.addEventListener('resize', resize);
        resize();

        function random(min, max) {
            return Math.random() * (max - min) + min;
        }

        class Particle {
            constructor() {
                this.x = random(0, width);
                this.y = random(-height, 0);
                this.size = random(5, 12);
                this.speedY = random(2, 6);
                this.speedX = random(-1, 1);
                this.rotation = random(0, 360);
                this.rotationSpeed = random(-5, 5);
                this.color = colors[Math.floor(random(0, colors.length))];
                this.shape = Math.random() > 0.5 ? 'rect' : 'circle';
            }

            update() {
                this.y += this.speedY;
                this.x += this.speedX;
                this.rotation += this.rotationSpeed;
                // Reset if off screen
                if (this.y > height + 20) {
                    this.y = -20;
                    this.x = random(0, width);
                }
                if (this.x > width + 20) this.x = -20;
                if (this.x < -20) this.x = width + 20;
            }

            draw() {
                ctx.save();
                ctx.translate(this.x, this.y);
                ctx.rotate((this.rotation * Math.PI) / 180);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = 0.9;
                if (this.shape === 'rect') {
                    ctx.fillRect(-this.size / 2, -this.size / 4, this.size, this.size / 2);
                } else {
                    ctx.beginPath();
                    ctx.arc(0, 0, this.size / 2, 0, Math.PI * 2);
                    ctx.fill();
                }
                ctx.restore();
            }
        }

        // Create initial particles
        function createParticles(count) {
            for (let i = 0; i < count; i++) {
                particles.push(new Particle());
            }
        }
        createParticles(120);

        function animate() {
            ctx.clearRect(0, 0, width, height);
            particles.forEach(p => {
                p.update();
                p.draw();
            });
            requestAnimationFrame(animate);
        }
        animate();
    })();

    // ===================== DISMISS BUTTON =====================
    function dismiss() {
        // Attempt to close the pywebview window
        window.close();
    }
</script>
</body>
</html>
"""

if __name__ == '__main__':
    # Create the window with a fixed size and a modern title
    window = webview.create_window(
        title='🎉 Nga, you made it!',
        html=HTML,
        width=800,
        height=600,
        resizable=True,
        fullscreen=False,
        confirm_close=False
    )
    webview.start()
