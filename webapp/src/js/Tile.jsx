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
        if (path !== '') {
            // Some older tiles have their paths prefixed with Assets_Content_Textures
            path = path.toLowerCase();
            let result = /^assets_content_textures_([a-zA-Z0-9\-]*)_(.*)$/.exec(path);
            if (result !== null) {
                this.path = '/textures/' + result[1] + '/' + result[2];
            }
            else {
                this.path = '/textures/' + path;
            }
        }
        else {
            this.path = null;
        }

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

    consoleTile() {
        // Retrieve the "tile" for the character when we're in console mode
        try {
            if (this.renderString === null || this.renderString.length === 0)
                throw new Error('missing RenderString for tile');

            const charCode = (this.renderString.length === 1)
                ? this.renderString.charCodeAt(0)
                : parseInt(this.renderString);

            if (charCode < 0 || charCode > 255)
                throw new Error(`charCode out of range: ${charCode}`);

            return `textures/text/${charCode}.bmp`
        }
        catch (err) {
            console.error(`Error determining render string: ${err}`);
            return 'textures/text/63.bmp';
        }
    }

    render(canvas, showBackground = true, enableTiles = true) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                this._render(canvas, img, showBackground, enableTiles);
                resolve(undefined);
            };
            img.onerror = reject;

            if (enableTiles && this.path !== null)
                img.src = this.path;
            else {
                enableTiles = false;
                img.src = this.consoleTile();
            }
        });
    }

    _render(canvas, img, showBackground, enableTiles) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        const primary = COLORMAP[this.fgColor()];
        const secondary = COLORMAP[this.detailColor];
        const bgColorStr = this.bgColor();

        if (enableTiles && this.hflip) {
            ctx.translate(canvas.width, 0);
            ctx.scale(-1, 1);
        }
        if (enableTiles && this.vflip) {
            ctx.translate(0, canvas.height);
            ctx.scale(1, -1);
        }

        ctx.drawImage(img, 0, 0);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = (!enableTiles)
            ? this._colorImageConsoleMode(imageData.data, primary, secondary)
            : this._colorImage(imageData.data, primary, secondary);

        ctx.putImageData(imageData, 0, 0);

        if (showBackground && bgColorStr in COLORMAP) {
            let color = COLORMAP[bgColorStr];
            color = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
            ctx.globalCompositeOperation = 'destination-over'
            ctx.fillStyle = color;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }
    }

    _colorImage(data, primary, secondary) {
        for (let i = 0; i < data.length; i += 4) {
            const weight = (data[i] === 0) ? 0 : 1;

            for (let j = 0; j < 3; j++) {
                // Weighted average of color channels for primary and
                // detail colors.
                const pixelColor = (1 - weight) * primary[j] + weight * secondary[j];
                data[i + j] = pixelColor;
            }
        }

        return data;
    }

    _colorImageConsoleMode(data, primary, secondary) {
        for (let i = 0; i < data.length; i += 4) {
            let alpha = 0;

            for (let j = 0; j < 3; j++) {
                alpha += data[i + j];
                data[i + j] = primary[j];
            }

            data[i + 3] = alpha / 3;
        }

        return data;
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
