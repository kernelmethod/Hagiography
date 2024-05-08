import { COLORMAP } from '$js/Color.jsx';

function capitalize(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}

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
        this.path = "/Textures/" + capitalize(path);
        this.renderString = renderString;
        this.colorString = new ColorString(colorString);
        this.detailColor = detailColor;
        this.tileColor = tileColor;
        this.hflip = hflip;
        this.vflip = vflip;
    }

    fgColor() {
        return this.colorString.fgColor || 'y';
    }

    bgColor() {
        return this.tileColor || this.colorString.bgColor;
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
