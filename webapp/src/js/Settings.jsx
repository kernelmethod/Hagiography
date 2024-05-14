import { browser } from '$app/environment';
import { writable } from 'svelte/store';

function getEnableTilesStore() {
    if (!browser)
        return writable(null);

    const { subscribe, set, update } = writable(null);
    const storedValue = localStorage.getItem('enableTiles');
    const initialValue = (storedValue === null)
        ? true
        : (storedValue === '1');
    console.log(initialValue);
    set(initialValue);

    return {
        subscribe,
        enable: () => {
            localStorage.setItem('enableTiles', '1');
            set(true);
        },
        disable: () => {
            localStorage.setItem('enableTiles', '0');
            set(false);
        },
        toggle: (value) => {
            localStorage.setItem('enableTiles', (value === true) ? '1' : '0');
            set(value === true);
        },
    };
}

export const enableTiles = getEnableTilesStore();
