<script>
  import { onMount } from 'svelte';
  import { parseTileSpec } from '$js/Tile.jsx';

  import ColorizedText from '$components/ColorizedText.svelte';
  import JournalSnapshot from '$components/record/JournalSnapshot.svelte';

  export let text;
  export let snapshot;

  let snapshotEl;
  let expanded = false;
  const collapsibleId = crypto.randomUUID();

  let snapshotPromise = null;
  let tiles = snapshot.split('|').map(parseTileSpec);

  export const hide = () => (expanded = false)
  export const show = () => (expanded = true)
  export const toggle = () => (expanded = !expanded)
</script>

<style lang="postcss">
  .collapsed {
    margin-top: -100%;
    transition: margin 0.25s ease-in;
    transition-delay: 0s;
  }

  .expanded {
    margin-top: 0;
    transition: margin 1s ease-out;
    transition-duration: 2s;
    transition-delay: -2s;
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
    <button aria-label="Expand entry" aria-controls={collapsibleId} aria-expanded={expanded} class="p-2 rounded-sm" on:click={toggle}>
      <span class="entry-prefix">$</span>
      <ColorizedText text={text} bold={false} />
    </button>
  </p>

  <div class="overflow-hidden">
    <div id={collapsibleId}
      bind:this={snapshotEl}
      class="text-center py-8"
      class:expanded={expanded}
      class:collapsed={!expanded}>
      <div class="flex flex-row justify-center min-h-96">
        {#if expanded}
        <!--
          Conditionally render snapshot to preserve memory and reduce compute when snapshots
          have to be updated.
        -->
        <JournalSnapshot tiles={tiles} />
        {/if}
      </div>
    </div>
  </div>
</div>
