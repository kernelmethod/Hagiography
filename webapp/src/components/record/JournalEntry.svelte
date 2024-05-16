<script>
  import { onMount } from 'svelte';
  import { parseTileSpec } from '$js/Tile.jsx';

  import ColorizedText from '$components/ColorizedText.svelte';
  import JournalSnapshot from '$components/record/JournalSnapshot.svelte';
  import Modal from '$components/Modal.svelte';

  export let text;
  export let snapshot;

  let journalEntryModal = null;
  let modalVisible = false;
  const collapsibleId = crypto.randomUUID();

  let snapshotPromise = null;
  let tiles = snapshot.split('|').map(parseTileSpec);

  export const show = () => {
    journalEntryModal.show();
  }
</script>

<style lang="postcss">
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
    <button
      aria-label="Expand entry"
      aria-controls={(journalEntryModal !== null) ? journalEntryModal.id : undefined}
      class="p-2 rounded-sm flex flex-row"
      on:click={show}>

      <span class="entry-prefix">$</span>
      <div class="pl-2">
        <ColorizedText text={text} bold={false} />
      </div>
    </button>
  </p>
</div>

<Modal bind:visible={modalVisible} bind:this={journalEntryModal}>
  <div slot="modalBody">
    {#if journalEntryModal !== null && modalVisible}
      <!--
      Conditionally render snapshot to preserve memory and reduce compute
      when snapshots have to be updated.
      -->
    <div class="flex flex-row justify-center">
      <JournalSnapshot tiles={tiles} />
    </div>
    <div class="text-center pt-4 italic text-balance">
      <ColorizedText text={text} bold={false} />
    </div>
    {/if}
  </div>
</Modal>
