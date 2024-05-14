import { browser } from '$app/environment';
import { writable } from 'svelte/store';

function getConsoleModeStore() {
    if (!browser)
        return writable(null);

    const { subscribe, set, update } = writable(null);
    const storedValue = localStorage.getItem('consoleMode');
    const initialValue = (storedValue === '0');
    set(initialValue);

    return {
        subscribe,
        enable: () => {
            localStorage.setItem('consoleMode', '1');
            set(true);
        },
        disable: () => {
            localStorage.setItem('consoleMode', '0');
            set(false);
        },
    };
}

export const consoleMode = getConsoleModeStore();
