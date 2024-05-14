<script>
  import { onMount, onDestroy } from 'svelte';
  import { COLORMAP } from '$js/Color.jsx';
  import { ColorString } from '$js/Tile.jsx';

  import { enableTiles } from '$js/Settings.jsx';

  let canvas = null;
  let renderPromise;
  let _enableTiles = true;

  export let tile;
  export let showBackground = true;

  const unsubscribe = enableTiles.subscribe((value) => {
    _enableTiles = value;
    if (canvas !== null)
      renderPromise = tile.render(canvas, showBackground, value);
  });

  onDestroy(unsubscribe);

  onMount(() => {
    renderPromise = tile.render(canvas, showBackground, _enableTiles);
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
