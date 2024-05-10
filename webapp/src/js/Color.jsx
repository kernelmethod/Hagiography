Array.prototype.randomChoice = function () {
    return this[Math.floor((Math.random()*this.length))];
}

const COLORMAP = {
    'r': [0xa6, 0x4a, 0x2e],
    'R': [0xd7, 0x42, 0x00],
    'o': [0xf1, 0x5f, 0x22],
    'O': [0xe9, 0x9f, 0x10],
    'w': [0x98, 0x87, 0x5f],
    'W': [0xcf, 0xc0, 0x41],
    'g': [0x00, 0x94, 0x03],
    'G': [0x00, 0xc4, 0x20],
    'b': [0x00, 0x48, 0xbd],
    'B': [0x00, 0x96, 0xff],
    'c': [0x40, 0xa4, 0xb9],
    'C': [0x77, 0xbf, 0xcf],
    'm': [0xb1, 0x54, 0xcf],
    'M': [0xda, 0x5b, 0xd6],
    'k': [0x0f, 0x3b, 0x3a],
    'K': [0x15, 0x53, 0x52],
    'y': [0xb1, 0xc9, 0xc3],
    'Y': [0xff, 0xff, 0xff]
};

const SHADERS = {
    'hologram': () => new Shader('b-B-C-c', 'sequence'),
    'ydfreehold': () => new Shader('r-R-k-c-C-W-W-C-c-r-R', 'sequence'),
    'purple': () => new Shader('m', 'sequence'),
    'paisley': () => new Shader('m-M-Y-M-m', 'sequence'),
    'biomech': () => new Shader('w-w-r-r-r-w-r-r', 'sequence'),
    'azure': () => new Shader('B', 'sequence'),
    'camouflage': () => new Shader('g-g-G-g-K-g-g-G-G-K', 'sequence'),
    'rainbow': () => new Shader('r-R-W-G-B-b-m', 'alternation'),
    'metamorphic': () => new Shader('y-y-y-Y-Y-Y-M-M-M-m-m-m-m', 'sequence'),
    'transkinetic': () => new Shader('Y-C-C-c-y-K-K-y-R-W-W-Y', 'sequence'),
    'dark red': () => new Shader('r', 'sequence'),
    'ubernostrum': () => new Shader('c-g-G-W-w-c-C-G-g-w-W', 'sequence'),
    'desert camouflage': () => new Shader('w-w-W-w-K-w-w-W-W-K', 'sequence'),
    'rocket': () => new Shader('Y-W-R-R-r-y', 'alternation'),
    'rubbergum': () => new Shader('W-W-w-w-y-y-Y-W-W', 'sequence'),
    'visage': () => new Shader('R-r-b-B-Y-y', 'sequence'),
    'snail-encrusted': () => new Shader('w-W-Y-y', 'sequence'),
    'dreamsmoke': () => new Shader('b-b-b-b-y-Y-Y-W-w-b-b-b', 'sequence'),
    'polarized': () => new Shader('K-y-Y-y-K-y-Y-y-K', 'alternation'),
    'ironshank': () => new Shader('K-y-Y-y', 'sequence'),
    'gold': () => new Shader('W', 'sequence'),
    'dark fiery': () => new Shader('r-R-W-R-r', 'alternation'),
    'bethsaida': () => new Shader('w-W-C-c-m-c-C-W-w', 'sequence'),
    'filthy': () => new Shader('w-w-K-w-K-w-W', 'sequence'),
    'sun': () => new Shader('W-R-W', 'alternation'),
    'pearly': () => new Shader('Y-Y-y', 'sequence'),
    'cider': () => new Shader('r', 'solid'),
    'engraved': () => new Shader('Y-y-c-C', 'sequence'),
    'coated in plasma': () => new Shader('K-K-y-g-G-Y-k-Y-Y-k-Y-G-g-y-K-K', 'sequence'),
    'gaslight': () => new Shader('g-g-w-W-w-g-g', 'alternation'),
    'entropic': () => new Shader('K-K-m-K-K-K-m-m-K-K-y', 'sequence'),
    'neutronic': () => new Shader('B-b-K-y-Y', 'sequence'),
    'lanterned': () => new Shader('y-y-y-y-Y-W-Y-y-y', 'alternation'),
    'dark magenta': () => new Shader('m', 'sequence'),
    'scarlet': () => new Shader('R', 'sequence'),
    'overloaded': () => new Shader('y-y-w-W-R-W-w-y-y', 'alternation'),
    'dark blue': () => new Shader('b', 'sequence'),
    'red': () => new Shader('R', 'sequence'),
    'patchwork': () => new Shader('W-w-r-R-W-w-b-B-W', 'sequence'),
    'nanotech': () => new Shader('K-K-y-K', 'sequence'),
    'brainbrine': () => new Shader('g-g-g-w-W-W-W-w-g-g-g', 'sequence'),
    'teal': () => new Shader('c', 'sequence'),
    'bee': () => new Shader('K-w-W-Y-W-w-K', 'alternation'),
    'cryogenic': () => new Shader('Y-C-C-Y-c-c-K-y-Y', 'sequence'),
    'eater': () => new Shader('Y-Y-M-Y-Y-Y', 'sequence'),
    'C': () => new Shader('C', 'sequence'),
    'B': () => new Shader('B', 'sequence'),
    'G': () => new Shader('G', 'sequence'),
    'dark orange': () => new Shader('o', 'sequence'),
    'feathered': () => new Shader('C-B-b-g-G-g-b-B-C', 'alternation'),
    'K': () => new Shader('K', 'sequence'),
    'M': () => new Shader('M', 'sequence'),
    'O': () => new Shader('O', 'sequence'),
    'internals': () => new Shader('W', 'solid'),
    'R': () => new Shader('R', 'sequence'),
    'prismatic': () => new Shader('r-R-W-G-B-b-m', 'sequence'),
    'W': () => new Shader('W', 'sequence'),
    'lovesickness': () => new Shader('r-R-M-m-r-R-M', 'sequence'),
    'Y': () => new Shader('Y', 'sequence'),
    'fiery': () => new Shader('R', 'sequence'),
    'urban camouflage': () => new Shader('y-y-K-y-K-y-y-K-y-K', 'sequence'),
    'crimson': () => new Shader('r', 'sequence'),
    'leopard': () => new Shader('W-W-w-w-W-K-K-w-w-W-W', 'sequence'),
    'glittering': () => new Shader('K-K-y-M-y-K-K', 'sequence'),
    'ghostly': () => new Shader('Y-Y-y-y-K-K', 'alternation'),
    'palladium mesh': () => new Shader('c-c-c-c-C-W-Y-W-C', 'sequence'),
    'tarnished': () => new Shader('G-G-g', 'sequence'),
    'c': () => new Shader('c', 'sequence'),
    'b': () => new Shader('b', 'sequence'),
    'shimmering': () => new Shader('Y-Y-y-y-K-K-y-y', 'sequence'),
    'g': () => new Shader('g', 'sequence'),
    'earth': () => new Shader('b-B-W-g-G', 'sequence'),
    'k': () => new Shader('k', 'sequence'),
    'qon': () => new Shader('m-b-B', 'sequence'),
    'm': () => new Shader('m', 'sequence'),
    'leafy': () => new Shader('g-g-G', 'sequence'),
    'o': () => new Shader('o', 'sequence'),
    'nectar': () => new Shader('W-w-g-G', 'sequence'),
    'shugruith': () => new Shader('K-y-W-w-m-w-W-y-K', 'sequence'),
    'putrid': () => new Shader('K', 'solid'),
    'agolgot': () => new Shader('K-g-w-m-w-g-K', 'sequence'),
    'r': () => new Shader('r', 'sequence'),
    'plasma': () => new Shader('g-G-Y-Y-G-g', 'sequence'),
    'love': () => new Shader('Y-R-Y-Y', 'sequence'),
    'w': () => new Shader('w', 'sequence'),
    'zetachrome': () => new Shader('m-M-Y-C-c-c-C-Y-M-m', 'alternation'),
    'y': () => new Shader('y', 'sequence'),
    'watery': () => new Shader('B-C-Y-C-B', 'alternation'),
    'black': () => new Shader('K', 'sequence'),
    'turbow': () => new Shader('K-y-Y-Y-R-r', 'sequence'),
    'psychalflesh': () => new Shader('w-w-w-r-R-M-M-m-M-M-R-r-w-w-w-w', 'sequence'),
    'yellow': () => new Shader('W', 'sequence'),
    'thermo': () => new Shader('R-R-r-c-b-B-B', 'sequence'),
    'white': () => new Shader('Y', 'sequence'),
    'telemetric': () => new Shader('K-y-c-C-Y-W-C-c-y-K', 'alternation'),
    'metachrome': () => new Shader('w-W-Y-C-c-c-C-Y-W-w', 'alternation'),
    'tartan': () => new Shader('y-K-g-G-K-R-r-K-y', 'sequence'),
    'plastifer': () => new Shader('K-y-Y-y', 'sequence'),
    'psymeridian': () => new Shader('K-K-y-y-y-m-M-M-M-M-m-y-y-y-K-K', 'sequence'),
    'sunslag': () => new Shader('r-W-Y-Y-Y-W-r', 'sequence'),
    'extradimensional': () => new Shader('M-M-m-m-y-y-Y-Y-O-Y-Y-y-m-m-M-M', 'alternation'),
    'sunset': () => new Shader('b-B-B-M-m-r-R-W-C-C-W-R-r-m-M-B-B-b', 'alternation'),
    'blaze': () => new Shader('r-r-R-W-Y', 'sequence'),
    'structural': () => new Shader('Y-y-K-y-Y', 'alternation'),
    'amorous': () => new Shader('r-R-M-m', 'alternation'),
    'starry': () => new Shader('K-Y-K-K-Y-K', 'sequence'),
    'refractive': () => new Shader('y-Y', 'sequence'),
    'spiked': () => new Shader('R-Y', 'bordered'),
    'sphynx': () => new Shader('C-c-m-M', 'sequence'),
    'spaser': () => new Shader('K-g-G-G-g-K', 'sequence'),
    'olive': () => new Shader('g-g-G-W-w', 'sequence'),
    'magenta': () => new Shader('M', 'sequence'),
    'soul': () => new Shader('W-w-c-C-Y-C-c-w-W', 'alternation'),
    'graffitied': () => new Shader('R-r-w-W-Y-y-r-R-W-w', 'sequence'),
    'snakeskin': () => new Shader('g-c-C-G', 'sequence'),
    'slimy': () => new Shader('g', 'solid'),
    'skulk': () => new Shader('b-b-B-b-b', 'sequence'),
    'dark gray': () => new Shader('K', 'sequence'),
    'silvery': () => new Shader('Y', 'sequence'),
    'rusty': () => new Shader('r', 'sequence'),
    'playernotes': () => new Shader('Y', 'solid'),
    'green': () => new Shader('G', 'sequence'),
    'fungicide': () => new Shader('M-M-R-r-K-r-R', 'sequence'),
    'nervous': () => new Shader('g-g-w-W-w-g-g', 'sequence'),
    'hotkey': () => new Shader('W', 'solid'),
    'gray': () => new Shader('y', 'sequence'),
    'jungle': () => new Shader('g-g-w-G-g-m-g-w-w-K-g-m-G-G-w', 'sequence'),
    'shemesh': () => new Shader('r-r-R-R-W-W-Y', 'sequence'),
    'cloning': () => new Shader('Y-Y-Y-Y-Y-Y-M-Y-M-Y-Y-Y-Y-Y-Y', 'sequence'),
    'lacquered': () => new Shader('Y-y-K-y-Y-y-K-y-Y-y', 'sequence'),
    'shade': () => new Shader('y-K-c-b-B-y-C-y-K', 'sequence'),
    'scaled': () => new Shader('g-G-W-w-g-G', 'sequence'),
    'bio': () => new Shader('g-G-W-M-W-G-g-g-g-g-g', 'sequence'),
    'rules': () => new Shader('C', 'solid'),
    'psionic': () => new Shader('b-B-C-c-b-B-C', 'alternation'),
    'spring-turret': () => new Shader('c-c-C-C-y-y-y-y-y-C-C-c-c', 'sequence'),
    'glotrot': () => new Shader('K-K-r-R-r', 'sequence'),
    'mercurial': () => new Shader('c-c-C-W-Y-W-C-c-c', 'alternation'),
    'peridot': () => new Shader('G-g-w-W-Y-W-G', 'sequence'),
    'crystalline': () => new Shader('m-m-m-b-B-Y-B-b-m-m-m', 'sequence'),
    'rermadon': () => new Shader('Y-G-g-m-m-g-G-Y', 'sequence'),
    'resonance': () => new Shader('c-c-C-C-W-C-C-c-c', 'alternation'),
    'crochide': () => new Shader('g-g-g-g-g-G', 'sequence'),
    'plaid': () => new Shader('g-K-G-W-G', 'sequence'),
    'syphon': () => new Shader('c-c-c-C-W-Y', 'sequence'),
    'cloudy': () => new Shader('y-y-Y-y-Y-Y', 'sequence'),
    'quantum': () => new Shader('m-m-m-m-m-m-m-Y-Y-Y-Y-Y', 'sequence'),
    'nanoneuro': () => new Shader('r-R-G-g-K-K-g-G-R-r-g', 'sequence'),
    'brown': () => new Shader('w', 'sequence'),
    'arctic camouflage': () => new Shader('y-y-Y-y-K-y-y-Y-Y-K', 'sequence'),
    'astral': () => new Shader('Y-y-K-y-Y', 'alternation'),
    'sparkling': () => new Shader('y-y-Y', 'sequence'),
    'kesil': () => new Shader('m-m-M-Y-y', 'sequence'),
    'hypertractor': () => new Shader('r-R-W-w-c-C-B-b', 'sequence'),
    'horned': () => new Shader('y-W', 'bordered'),
    'defoliant': () => new Shader('W-W-G-g-K-g-G', 'sequence'),
    'ninefold': () => new Shader('b-B', 'bordered'),
    'sickly': () => new Shader('g-r-m-w-K-G-g-c-K', 'sequence'),
    'painted': () => new Shader('r-R-W-w-g-G-B', 'sequence'),
    'moon': () => new Shader('b-B-C-c', 'sequence'),
    'mirrorshades': () => new Shader('K-y-Y-Y-y-K', 'sequence'),
    'dark cyan': () => new Shader('c', 'sequence'),
    'dark green': () => new Shader('g', 'sequence'),
    'radiant': () => new Shader('r-W-Y-Y-Y-W-r', 'sequence'),
    'issachari': () => new Shader('Y-Y-Y-Y-Y-Y-r', 'sequence'),
    'qas': () => new Shader('C-c-m', 'sequence'),
    'lava': () => new Shader('R', 'solid'),
    'lah': () => new Shader('w-W-R-r', 'sequence'),
    'normalish': () => new Shader('y-y-K-y-Y-y-y-y-K-y-Y', 'sequence'),
    'kaleidoslug': () => new Shader('K-C-y-m-M-r-c-C-Y-y-K', 'sequence'),
    'levant': () => new Shader('r-r-y-y-Y-Y', 'sequence'),
    'beylah': () => new Shader('B-b-g-k-W-R-r', 'sequence'),
    'illuminated': () => new Shader('c-c-c-C-Y-W-Y-C', 'sequence'),
    'icy': () => new Shader('Y-C-B-C-Y', 'alternation'),
    'normal': () => new Shader('K-K-y-y-Y-y-y-K-K-y-K-y-Y', 'sequence'),
    'freezing': () => new Shader('C', 'sequence'),
    'blue': () => new Shader('B', 'sequence'),
    'forest': () => new Shader('g-g-w-G-g-g-w-w-g-G-G-w', 'sequence'),
    'emote': () => new Shader('w', 'solid'),
    'electrical': () => new Shader('W', 'sequence'),
    'dreamy': () => new Shader('b-b-b-B-M-k-W-M-B-b-b-b-b', 'alternation'),
    'crysteel': () => new Shader('y-y-K-g-g-K-y-y', 'alternation'),
    'phase-harmonic': () => new Shader('Y-y-m-y-K', 'sequence'),
    'chiral': () => new Shader('B-b-c-C-M-m-k-m-M-C-c-b', 'sequence'),
    'implanted': () => new Shader('r-r-r-r-r-r-r-C', 'sequence'),
    'auroral': () => new Shader('K-g-G-Y-G-g-K', 'sequence'),
    'opalescent': () => new Shader('Y-y-K-K-y-Y', 'sequence'),
    'cyan': () => new Shader('C', 'sequence'),
    'otherpearl': () => new Shader('M-m-y-Y-O-O-Y-y-m-M', 'sequence'),
    'orange': () => new Shader('O', 'sequence'),
};

/**
 * Return the CSS class corresponding to a color specifier (one of the colors
 * defined in COLORMAP).
 *
 * @param {string} colorChar - The character corresponding to the color specification.
 * @return {string} The CSS class corresponding to the color.
 * @throws Will throw an error if colorChar does not correspond to any known color.
 */
function getColorClass(colorChar) {
    if (colorChar in COLORMAP)
        return 'qudcolor-' + colorChar;
    throw new Error(`unknown color specifier '${colorChar}'`);
}

class ColorizedText {
    constructor(text, colorChar) {
        this.text = text;
        this.colorClass = getColorClass(colorChar);
    }
}

class Shader {
    constructor(colors, type) {
        this.colors = colors.split('-');
        this.type = type;
    }

    shadeText(text) {
        switch (this.type) {
            case 'solid':
                return this._shadeSolid(text);
            case 'sequence':
                return this._shadeSequence(text);
            case 'alternation':
                return this._shadeAlternation(text);
            case 'chaotic':
                return this._shadeChaotic(text);
            case 'bordered':
                return this._shadeBordered(text);
            default:
                throw new Error(`unknown shader type ${this.type}`);
        }
    }

    _shadeSolid(text) {
        return [new ColorizedText(text, this.colors[0])];
    }

    _shadeSequence(text) {
        if (this.colors.length === 1)
            return this._shadeSolid(text);

        let output = [];
        for (let i = 0; i < text.length; i++) {
            let color = this.colors[i % this.colors.length];
            output.push(new ColorizedText(text.charAt(i), color));
        }

        return output;
    }

    _shadeAlternation(text) {
        if (this.colors.length === 1)
            return this._shadeSolid(text);

        let output = [];
        for (let i = 0; i < text.length; i++) {
            let color = this.colors[Math.floor(i / text.length * this.colors.length)];
            output.push(new ColorizedText(text.charAt(i), color));
        }

        return output;
    }

    _shadeChaotic(text) {
        if (this.colors.length === 1)
            return this._shadeSolid(text);

        let output = [];
        for (let i = 0; i < text.length; i++) {
            output.push(new ColorizedText(text.charAt(i), this.colors.randomChoice()));
        }

        return output;
    }

    _shadeBordered(text) {
        if (this.colors.length !== 2)
            throw new Error(`bordered shaders must have exactly two colors; got ${this.colors}`);

        if (text.length === 0)
            return [];
        if (text.length === 1)
            return [new ColorizedText(text.charAt(0), this.colors[0])];

        let output = [];
        output.push(new ColorizedText(text.charAt(0), this.colors[0]));

        let middle = text.substring(1, text.length - 1);
        if (middle.length > 0) {
            output.push(new ColorizedText(middle, this.colors[1]));
        }

        output.push(new ColorizedText(text.charAt(text.length - 1), this.colors[0]));
        return output;
    }
}

class ShadedFragment {
    constructor(text, shader) {
        this.text = text;

        if (shader === null) {
            this.shader = new Shader('y', 'solid');
            return;
        }

        const re = /^[A-z](?:-[A-z])* [A-z]+$/;
        const match = re.exec(shader);
        if (match !== null) {
            let [ colors, type ] = shader.split(' ');
            this.shader = new Shader(colors, type);
        }
        else {
            let s = SHADERS[shader];
            if (s === undefined)
                throw new Error(`unknown shader ${shader}`);
            this.shader = s();
        }
    }

    getColorizedFragments() {
        return this.shader.shadeText(this.text);
    }
}

function parseTextColorization(text, currentColor = 'Y') {
    // ref: https://github.com/TrashMonks/hagadias/blob/18f72afaa11c0aa21907b05133122ddaa4c6d82d/hagadias/helpers.py#L166
    // parser state
    const READING_TEXT = 1
    const ONE_LEFT_BRACE = 2
    const READING_SHADER = 3
    const ONE_RIGHT_BRACE = 4
    let state = READING_TEXT
    let shaderStack = []
    let currentShader = null; // default white
    let newShaderName = ""
    let coloredChars = []

    for (let i = 0; i < text.length; i++) {
        const char = text.charAt(i);

        if (state === READING_TEXT) {
            if (char == '{') {
                state = ONE_LEFT_BRACE;
            }
            else if (char == '}') {
                state = ONE_RIGHT_BRACE;
            }
            else {
                coloredChars.push([char, currentShader]);
            }
        }
        else if (state === ONE_LEFT_BRACE) {
            if (char == '{') {
                state = READING_SHADER;
            }
            else {
                state = READING_TEXT;
                coloredChars.push(['{', currentShader]);
                coloredChars.push([char, currentShader]);
            }
        }
        else if (state === READING_SHADER) {
            if (char === '|') {
                state = READING_TEXT;
                shaderStack.push(currentShader);
                currentShader = newShaderName;
                newShaderName = "";
            }
            else {
                newShaderName += char;
            }
        }
        else {    // ONE_RIGHT_BRACE
            if (char === '}') {
                if (shaderStack.length === 0) {
                    throw new Error(`Unexpected }} while parsing ${text}`);
                }
                else {
                    currentShader = shaderStack.pop();
                }
            }
            else {
                coloredChars.push([char, currentShader]);
            }
        }
    }

    // Conflate sequential chars with the same shader
    let output = [];
    currentShader = null;
    let currentFragment = "";

    for (let i = 0; i < coloredChars.length; i++) {
        let [ char, color ] = coloredChars[i];

        if (color === currentShader) {
            currentFragment += char;
        }
        else {
            if (currentFragment.length > 0) {
                output.push(new ShadedFragment(currentFragment, currentShader));
            }
            currentFragment = char;
            currentShader = color;
        }
    }

    if (currentFragment.length > 0)
        output.push(new ShadedFragment(currentFragment, currentShader));

    return output;
}

export {
    COLORMAP,
    ShadedFragment,
    parseTextColorization
} 
