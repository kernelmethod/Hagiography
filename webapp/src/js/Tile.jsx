import { COLORMAP } from '$js/Color.jsx';

class Tile {
    constructor(
        path,
        renderString,
        colorString,
        detailColor,
        tileColor,
        hflip = false,
        vflip = false
    ) {
        // Some older tiles have their paths prefixed with Assets_Content_Textures
        path = path.toLowerCase();
        let result = /^assets_content_textures_([a-zA-Z0-9\-]*)_(.*)$/.exec(path);
        if (result !== null) {
            this.path = '/textures/' + result[1] + '/' + result[2];
        }
        else {
            this.path = '/textures/' + path;
        }

        this.path = this.path.toLowerCase();
        this.renderString = renderString;
        this.colorString = new ColorString(colorString);
        this.detailColor = detailColor;
        this.tileColor = tileColor;
        this.hflip = hflip;
        this.vflip = vflip;
    }

    fgColor() {
        return this.tileColor || this.colorString.fgColor || 'y';
    }

    bgColor() {
        return this.colorString.bgColor;
    }

    render(canvas, showBackground = true) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                this._render(canvas, img, showBackground);
                resolve(undefined);
            };
            img.onerror = reject;
            img.src = this.path;
        });
    }

    _render(canvas, img, showBackground) {
        const ctx = canvas.getContext('2d');

        const primary = COLORMAP[this.fgColor()];
        const secondary = COLORMAP[this.detailColor];
        const bgColorStr = this.bgColor();

        if (this.hflip) {
            ctx.translate(canvas.width, 0);
            ctx.scale(-1, 1);
        }
        if (this.vflip) {
            ctx.translate(0, canvas.height);
            ctx.scale(1, -1);
        }

        ctx.drawImage(img, 0, 0);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
            let weight = (data[i] === 255) ? 1 : 0;

            for (let j = 0; j < 3; j++) {
                // Weighted average of color channels for primary and
                // detail colors.
                const pixelColor = (1 - weight) * primary[j] + weight * secondary[j];
                data[i + j] = pixelColor;
            }
        }

        ctx.putImageData(imageData, 0, 0);

        if (showBackground && bgColorStr in COLORMAP) {
            let color = COLORMAP[bgColorStr];
            color = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
            ctx.globalCompositeOperation = 'destination-over'
            ctx.fillStyle = color;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }
    }
}

class ColorString {
    constructor(colorString) {
        // ex. y
        if (colorString in COLORMAP) {
            this.fgColor = colorString;
            this.bgColor = null;
            return;
        }

        // ex. &y
        let result = /^&(.)$/.exec(colorString);
        if (result !== null) {
            this.fgColor = result[1];
            this.bgColor = null;
            return;
        }

        // ex. &y^k
        result = /^&(.)\^(.)$/.exec(colorString);
        if (result !== null) {
            this.fgColor = result[1];
            this.bgColor = result[2];
            return;
        }

        this.fgColor = null
        this.bgColor = null;
    }
}

function parseTileSpec(spec) {
    let components = spec.split(";");

    if (components.length !== 7)
        throw new Error("invalid tile spec");

    return new Tile(
        components[0],
        components[1],
        components[2],
        components[3],
        components[4],
        components[5] == "1",
        components[6] == "1"
    );
}

export {
    Tile,
    ColorString,
    parseTileSpec,
}
