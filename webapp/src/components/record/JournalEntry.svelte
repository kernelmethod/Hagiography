<script>
  import { onMount } from 'svelte';
  import { parseTileSpec } from '$js/Tile.jsx';

  import ColorizedText from '$components/ColorizedText.svelte';

  export let text;
  export let snapshot;

  let canvas;
  let snapshotPromise = null;
  let tiles = snapshot.split('|').map(parseTileSpec);

  async function drawSnapshot() {
    let subcanvases = [];
    let promises = [];

    for (let i = 0; i < tiles.length; i++) {
      const tile = tiles[i];
      const subcanvas = document.createElement('canvas');
      subcanvas.width = 16;
      subcanvas.height = 24;

      subcanvases.push(subcanvas);
      promises.push(tile.render(subcanvas, true));
    }

    const ctx = canvas.getContext('2d');

    for (let i = 0; i < tiles.length; i++) {
      try {
        await promises[i];
        const subcanvas = subcanvases[i];

        const cornerX = (i % 9) * 16;
        const cornerY = Math.trunc(i / 9) * 24;

        ctx.drawImage(subcanvas, cornerX, cornerY);
      }
      catch (e) {
        console.log(`snapshot render error: {e}`);
      }
    }

    // Color in background
    ctx.globalCompositeOperation = 'destination-over';
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }

  onMount(() => {
    snapshotPromise = drawSnapshot();
  });
</script>

<style>
  canvas {
    image-rendering: pixelated;
    min-width: 400px;
  }

  .snapshot {
    text-align: center;
    margin-top: 2em;
    margin-bottom: 2em;
  }

  .entry-prefix {
    color: var(--qudcolor-K);
  }
</style>

<div>
  <p>
    <span class="entry-prefix">$</span>
    <ColorizedText text={text} bold={false} />
  </p>

  <div class="snapshot">
    {#await snapshotPromise then}
    {/await}
    <canvas bind:this={canvas} width=144 height=120></canvas>
  </div>
</div>
