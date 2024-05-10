<script>
  import { onMount } from 'svelte';
  import { COLORMAP } from '$js/Color.jsx';
  import { ColorString } from '$js/Tile.jsx';

  let canvas;
  let renderPromise;

  export let tile;
  export let showBackground = true;

  onMount(() => {
    renderPromise = tile.render(canvas, showBackground);
  });
</script>

<style>
  canvas {
    height: var(--height, 100%);
    image-rendering: crisp-edges;
  }
</style>

{#await renderPromise then}
{/await}
<canvas bind:this={canvas} width=16 height=24></canvas>
