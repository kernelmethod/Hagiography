/* Utilities for build code parsing. */

import { Tile } from '$js/Tile.jsx';

class Subtype {
    constructor(Bonuses, Tile, DetailColor) {
        this.Bonuses = Bonuses;
        this.Tile = Tile;
        this.DetailColor = DetailColor;
    }

    getStat(statName) {
        return 10 + (this.Bonuses[statName] || 0);
    }

    Strength() { return this.getStat('Strength'); }
    Agility() { return this.getStat('Agility'); }
    Toughness() { return this.getStat('Toughness'); }
    Intelligence() { return this.getStat('Intelligence'); }
    Willpower() { return this.getStat('Willpower'); }
    Ego() { return this.getStat('Ego'); }

    getTile() {
        return new Tile(this.Tile, '@', 'y', this.DetailColor, 'y');
    }
}

const SUBTYPE_MAP = {
    // True Kin castes
    /// The Toxic Arboreta of Ekuemekiyye, the Holy City
    'Horticulturalist': () => new Subtype({Intelligence: 3}, 'creatures/caste_1.bmp' ,'g'),
    'Priest of All Suns': () => new Subtype({Ego: 3}, 'creatures/caste_2.bmp', 'Y'),
    'Priest of All Moons': () => new Subtype({Willpower: 2, Toughness: 2}, 'creatures/caste_3.bmp', 'W'),
    'Syzygyrior': () => new Subtype({Agility: 3}, 'creatures/caste_4.bmp', 'g'),

    /// The Ice-Sheathed Arcology of Ibul
    'Artifex': () => new Subtype({Intelligence: 3}, 'creatures/caste_5.bmp', 'c'),
    'Consul': () => new Subtype({Ego: 3}, 'creatures/caste_6.bmp', 'c'),
    'Praetorian': () => new Subtype({Strength: 2, Toughness: 1, Willpower: 1}, 'creatures/caste_7.bmp', 'c'),
    'Eunuch': () => new Subtype({Agility: 2, Intelligence: 2}, 'creatures/caste_8.bmp', 'c'),

    /// The Crustal Mortars of Yawningmoon
    'Child of the Hearth': () => new Subtype({Strength: 3}, 'creatures/caste_9.bmp', 'r'),
    'Child of the Wheel': () => new Subtype({Agility: 2, Strength: 1, Ego: 1}, 'creatures/caste_10.bmp', 'r'),
    'Child of the Deep': () => new Subtype({Toughness: 3}, 'creatures/caste_11.bmp', 'r'),
    'Fuming God-Child': () => new Subtype({Willpower: 4}, 'creatures/caste_12.bmp', 'r'),

    // Mutant human callings
    'Apostle': () => new Subtype({Ego: 2}, 'creatures/caste_13.bmp', 'm'),
    'Arconaut': () => new Subtype({Agility: 2}, 'creatures/caste_14.bmp', 'Y'),
    'Greybeard': () => new Subtype({Willpower: 3, Strength: -1}, 'creatures/caste_15.bmp', 'w'),
    'Gunslinger': () => new Subtype({Agility: 2}, 'creatures/caste_16.bmp', 'K'),
    'Marauder': () => new Subtype({Strength: 2}, 'creatures/caste_17.bmp', 'r'),
    'Pilgrim': () => new Subtype({Willpower: 2}, 'creatures/caste_18.bmp', 'y'),
    'Nomad': () => new Subtype({Toughness: 2}, 'creatures/caste_19.bmp', 'W'),
    'Scholar': () => new Subtype({Intelligence: 2}, 'creatures/caste_20.bmp', 'C'),
    'Tinker': () => new Subtype({Intelligence: 2}, 'creatures/caste_21.bmp', 'c'),
    'Warden': () => new Subtype({Strength: 2}, 'creatures/caste_22.bmp', 'w'),
    'Water Merchant': () => new Subtype({Ego: 2}, 'creatures/caste_23.bmp', 'B'),
    'Watervine Farmer': () => new Subtype({Toughness: 2}, 'creatures/caste_24.bmp', 'y'),
};

// Mapping of cybernetic ids to their true names
const CYBERNETIC_MAP = {
    'BiologicalIndexer': '{{Y|optical bioscanner}}',
    'TechnologicalIndexer': '{{Y|optical technoscanner}}',
    'CherubicVisage': '{{Y|cherubic visage}}',
    'DermalInsulation': '{{Y|dermal insulation}}',
    'HyperElasticAnkleTendons': '{{Y|hyper-elastic ankle tendons}}',
    'ParabolicMuscularSubroutine': '{{Y|parabolic muscular subroutine}}',
    'TranslucentSkin': '{{Y|translucent skin}}',
    'StabilizerArmLocks': '{{Y|stabilizer arm locks}}',
    'RapidReleaseFingerFlexors': '{{Y|rapid release finger flexors}}',
    'CarbideHandBones': '{{Y|carbide hand bones}}',
    'Pentaceps': '{{Y|pentaceps}}',
    'InflatableAxons': '{{Y|inflatable axons}}',
    'NocturnalApex': '{{Y|nocturnal apex}}',
    'AirCurrentMicrosensor': '{{Y|air current microsensor}}',
};

class Build {
    constructor(buildJson) {
        this._buildJson = buildJson;
    }

    getModule(moduleName) {
        for (let i = 0; i < this._buildJson.modules.length; i++) {
            const module = this._buildJson.modules[i];

            if (module.moduleType.includes(moduleName))
                return module;
        }

        return null;
    }

    getCyberneticsModule() {
        return this.getModule("XRL.CharacterBuilds.Qud.QudCyberneticsModule");
    }

    getMutationsModule() {
        return this.getModule("XRL.CharacterBuilds.Qud.QudMutationsModule");
    }

    getAttributesModule() {
        return this.getModule("XRL.CharacterBuilds.Qud.QudAttributesModule");
    }

    getSubtypeModule() {
        return this.getModule("XRL.CharacterBuilds.Qud.QudSubtypeModule");
    }
}

async function parseBuildCode(buildCode) {
    const ds = new DecompressionStream('gzip');

    // Base64-decode build code and convert it into a byte array
    const bcDecoded = atob(buildCode);
    const bytes = new Uint8Array(bcDecoded.length);

    for (let i = 0; i < bytes.length; i++)
        bytes[i] = bcDecoded.charCodeAt(i);

    // Decompress blob and convert to JSON
    const blob = new Blob([bytes]);
    const decompressedStream = blob.stream().pipeThrough(ds);
    const dCode = await new Response(decompressedStream).text();
    const build = JSON.parse(dCode);

    console.log(build);
    return new Build(build);
}

export {
    Build,
    Subtype,
    CYBERNETIC_MAP,
    SUBTYPE_MAP,
    parseBuildCode,
};
