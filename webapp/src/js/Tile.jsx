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
        this.path = path;
        this.renderString = renderString;
        this.colorString = colorString;
        this.detailColor = detailColor;
        this.tileColor = tileColor;
        this.hflip = hflip;
        this.vflip = vflip;
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
    parseTileSpec
}
