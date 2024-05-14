<script>
  import { onMount } from 'svelte';
  import { parseTileSpec } from '$js/Tile.jsx';

  import ColorizedText from '$components/ColorizedText.svelte';

  export let text;
  export let snapshot;

  let snapshotEl;

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

  export const hide = () => new bootstrap.Collapse(snapshotEl).hide();
  export const show = () => new bootstrap.Collapse(snapshotEl).show();
  export const toggle = () => new bootstrap.Collapse(snapshotEl).toggle();

  onMount(() => {
    snapshotEl.addEventListener('show.bs.collapse', event => {
      snapshotPromise = drawSnapshot();
    });

    snapshotEl.addEventListener('hidden.bs.collapse', event => {
      snapshotPromise = null;
    });
  });
</script>

<style>
  canvas {
    image-rendering: pixelated;
    min-width: 400px;
    padding: 0.5em;
    border: 2px dotted white;
  }

  .snapshot {
    text-align: center;
    margin-top: 2em;
    margin-bottom: 2em;
  }

  .entry-prefix {
    color: var(--qudcolor-K);
  }

  button {
    font-size: var(--bs-body-font-size);
    width: 100%;
    text-align: left;
  }

  button:hover {
    background-color: var(--highlight-color);
  }
</style>

<div>
  <p>
    <button class="btn" on:click={toggle}>
      <span class="entry-prefix">$</span>
      <ColorizedText text={text} bold={false} />
    </button>
  </p>

  <div bind:this={snapshotEl} class="snapshot collapse">
    {#if snapshotPromise !== null}
    {#await snapshotPromise then}
    {/await}
    {/if}
    <canvas bind:this={canvas} width=144 height=120>
    </canvas>
  </div>
</div>
