<script>
  import { onMount } from 'svelte';
  import { parseTileSpec } from '$js/Tile.jsx';

  import ColorizedText from '$components/ColorizedText.svelte';
  import JournalSnapshot from '$components/record/JournalSnapshot.svelte';

  export let text;
  export let snapshot;

  let snapshotEl;
  let collapsed = true;

  let snapshotPromise = null;
  let tiles = snapshot.split('|').map(parseTileSpec);

  export const hide = () => new bootstrap.Collapse(snapshotEl).hide();
  export const show = () => new bootstrap.Collapse(snapshotEl).show();
  export const toggle = () => new bootstrap.Collapse(snapshotEl).toggle();

  onMount(() => {
    snapshotEl.addEventListener('show.bs.collapse', event => {
      collapsed = false;
    });

    snapshotEl.addEventListener('hidden.bs.collapse', event => {
      collapsed = true;
    });
  });
</script>

<style>
  .snapshot {
    text-align: center;
    margin: 2em 0 2em 0;
    padding: 1em 0 1em 0;
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
    {#if !collapsed}
    <!--
      Conditionally render snapshot to preserve memory and reduce compute when snapshots
      have to be updated.
    -->
    <JournalSnapshot tiles={tiles} />
    {/if}
  </div>
</div>
