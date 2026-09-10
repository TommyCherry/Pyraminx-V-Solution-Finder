const canvas = document.getElementById("pyraminxCanvas");

canvas.width = window.innerWidth;
canvas.height = window.innerWidth < 600 ? 400 : 650;

const ctx = canvas.getContext("2d");

function drawTriangle(x1, y1, x2, y2, x3, y3, color, label="") {
    ctx.beginPath();

    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.lineTo(x3, y3);

    ctx.closePath();

    ctx.fillStyle = color;
    ctx.fill();

    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Find center of this triangle
    const centerX = (x1 + x2 + x3) / 3;
    const centerY = (y1 + y2 + y3) / 3;

    // Number styling
    ctx.fillStyle = "white";
    ctx.font = "16px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    // Draw the number (used for production, not user-facing)
    ctx.fillText(label, centerX, centerY);
}

function drawFace(topX, topY, size, colors) {
    const height = size * Math.sqrt(3) / 2;

    const rowHeight = height / 3;
    const halfStep = size / 6;

    let sticker = 0;

    for (let row = 0; row < 3; row++) {

        const yTop = topY + row * rowHeight;
        const yBottom = topY + (row + 1) * rowHeight;

        const rowLeft = topX - row * halfStep;
        const bottomLeft = topX - (row + 1) * halfStep;

        // Upward triangles
        for (let i = 0; i <= row; i++) {

            const xTop = rowLeft + i * (size / 3);
            const xBottomLeft = bottomLeft + i * (size / 3);
            const xBottomRight = xBottomLeft + size / 3;

            drawTriangle(
                xTop, yTop,
                xBottomLeft, yBottom,
                xBottomRight, yBottom,
                colors[sticker], sticker
            );

            sticker++;
        }

        // Downward triangles
        for (let i = 0; i < row; i++) {

            const xTopLeft = rowLeft + i * (size / 3);
            const xTopRight = xTopLeft + size / 3;
            const xBottom = bottomLeft + (i + 1) * (size / 3);

            drawTriangle(
                xTopLeft, yTop,
                xTopRight, yTop,
                xBottom, yBottom,
                colors[sticker], sticker
            );

            sticker++;
        }
    }
}

function drawRotatedFace(centerX, centerY, size, colors, rotation) {
    const height = size * Math.sqrt(3) / 2;

    ctx.save();

    // Move origin to center of the face
    ctx.translate(centerX, centerY);

    // Rotate
    ctx.rotate(rotation);

    // Draw face centered around the new origin
    drawFace(
        0,
        -height / 2,
        size,
        colors
    );

    ctx.restore();
}

const faceSize = 200;
const height = faceSize * Math.sqrt(3) / 2;

const centerX = canvas.width / 2;
const centerY = 100;

const redFace = faceColors.red;
const greenFace = faceColors.green;
const blueFace = faceColors.blue;
const yellowFace = faceColors.yellow;

// Upper-left face — upside down
drawRotatedFace(
    centerX - faceSize / 2,
    centerY,
    faceSize,
    redFace,
    Math.PI
);


// Upper-right face — upside down
drawRotatedFace(
    centerX + faceSize / 2,
    centerY,
    faceSize,
    blueFace,
    Math.PI
);


// Middle face — upright
drawRotatedFace(
    centerX,
    centerY,
    faceSize,
    greenFace,
    0
);


// Bottom face — upside down
drawRotatedFace(
    centerX,
    centerY + height,
    faceSize,
    yellowFace,
    Math.PI
);