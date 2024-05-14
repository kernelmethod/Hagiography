<script>
  import { onMount, onDestroy } from 'svelte';
  import { COLORMAP } from '$js/Color.jsx';
  import { ColorString } from '$js/Tile.jsx';

  import { consoleMode } from '$js/Settings.jsx';

  let canvas = null;
  let renderPromise;

  export let tile;
  export let showBackground = true;

  onMount(() => {
    const unsubscribe = consoleMode.subscribe((value) => {
      renderPromise = tile.render(canvas, showBackground, value);
    });

    onDestroy(unsubscribe);
  });
</script>

<style>
  canvas {
    height: var(--height, 100%);
    image-rendering: pixelated;
  }
</style>

{#await renderPromise then}
{/await}
<canvas bind:this={canvas} width=16 height=24></canvas>
