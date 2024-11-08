<script>
  import { onMount, onDestroy } from 'svelte';

  import { enableTiles } from '$js/Settings.jsx';

  export let tiles;

  let canvas = null;
  let snapshotPromise = null;
  let _enableTiles = true;

  let exitPromise = null;

  async function drawSnapshot() {
    let subcanvases = [];
    let promises = [];

    for (let i = 0; i < tiles.length; i++) {
      const tile = tiles[i];
      const subcanvas = document.createElement('canvas');
      subcanvas.width = 16;
      subcanvas.height = 24;

      subcanvases.push(subcanvas);
      promises.push(tile.render(subcanvas, true, _enableTiles));
    }

    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < tiles.length; i++) {
      try {
        await promises[i];
        const subcanvas = subcanvases[i];

        const cornerX = (i % 9) * 16;
        const cornerY = Math.trunc(i / 9) * 24;

        ctx.drawImage(subcanvas, cornerX, cornerY);
      }
      catch (e) {
        console.log(`snapshot render error: ${e}`);
      }
    }

    // Color in background
    ctx.globalCompositeOperation = 'destination-over';
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  const unsubscribe = enableTiles.subscribe((value) => {
    _enableTiles = value;
    if (canvas !== null)
      snapshotPromise = drawSnapshot();
  });

  onMount(() => {
    snapshotPromise = drawSnapshot();
  });

  onDestroy(unsubscribe);
</script>

<style lang="postcss">
  canvas {
    image-rendering: pixelated;
  }
</style>

{#if snapshotPromise !== null}
{#await snapshotPromise then}
{/await}
{/if}
<canvas
  bind:this={canvas}
  width=144
  height=120
  class:opacity-0={snapshotPromise === null}
  class:opacity-100={snapshotPromise !== null}
  class="w-64 md:w-96 h-full p-2 block border-2 border-dotted transition-opacity duration-500">
</canvas>
