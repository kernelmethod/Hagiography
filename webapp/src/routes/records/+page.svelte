<script>
  import { onMount } from "svelte";
  import ColorizedText from '$components/ColorizedText.svelte';
  import ClipboardWidget from '$components/ClipboardWidget.svelte';
  import DateTime from '$components/DateTime.svelte';
  import GameTileFromString from '$components/GameTileFromString.svelte';
  import Spinner from '$components/Spinner.svelte';
  import Modal from '$components/Modal.svelte';

  import BuildSummary from '$components/record/BuildSummary.svelte';
  import JournalEntry from '$components/record/JournalEntry.svelte';
  import RecordHeading from '$components/record/RecordHeading.svelte';

  const endpoint = '/api/records/id';

  let waitingForRecord = true;
  let record = null;
  let recordPromise = null;
  let journalPromise = null;

  let recordId;
  let buildCodeModal = null;

  async function fetchRecord() {
    await fetch('/api/records/id/' + recordId)
      .then(response => {
        if (response.status != 200)
          throw new Error('unable to retrieve record');
        return response.json();
      })
      .then(response => {
        record = response;
      })
      .finally(() => {
        waitingForRecord = false;
      });
  }

  async function fetchJournalEntries() {
    return await fetch(`/api/records/journal/list?id=${recordId}&start=0&end=50`)
      .then(response => {
        return response.json();
      })
      .then(response => {
        return response.entries;
      })
      .catch(err => {
        console.log(err);
        throw err;
      });
  }

  onMount(() => {
    const urlParams = new URLSearchParams(window.location.search);
    recordId = urlParams.get('id');
    recordPromise = fetchRecord();
    journalPromise = fetchJournalEntries();
  });
</script>

<style lang="postcss">
  .character-name {
    display: inline-block;
    padding-left: 1rem;
  }

  p {
    margin: 0;
  }
</style>

<main>
  {#if waitingForRecord}
  <div class="text-center">
    <Spinner --size="128px">
      Loading character data...
    </Spinner>
  </div>
  {/if}
  {#if recordPromise !== null}
  {#await recordPromise then}
  <div class="flex flex-row mb-4">
    <div>
      <GameTileFromString --height="128px" spec="{record.tile}" showBackground={false} />
    </div>
    <div>
      <div class="flex flex-col justify-center items-center text-5xl font-bold ml-8" style="height: 100%;">
        <ColorizedText text="{record.character_name}" />
      </div>
    </div>
  </div>

  <p><b>Game mode:</b> {record.game_mode}</p>
  <p><b>Score:</b> {record.score}</p>
  <p><b>Turns played:</b> {record.turns}</p>
  <p><b>Played on:</b> <DateTime timestamp="{record.created}" /></p>
  {:catch error}
  <h1 class="text-error">{error}</h1>
  {/await}

  <!-- Build -->

  <RecordHeading>
    Build
  </RecordHeading>

  {#if record !== null}
  {#if record.build_code !== undefined}
  <BuildSummary buildCode={record.build_code} />
  {:else}
  <p class="text-error">No build code was found for this game.</p>
  {/if}
  {/if}

  {#if buildCodeModal !== null}
  <p>
    <button type="button" class="btn btn-primary" on:click={() => buildCodeModal.show()}>
      Show build code
    </button>
  </p>
  {/if}

  <!-- Journal entries -->

  {#await journalPromise}
    <Spinner --size="96px">
      Loading journal data...
    </Spinner>
  {:then journalEntries}
    <RecordHeading>
      Journal entries
    </RecordHeading>
  {#if journalEntries.length === 0}
    <span class="fst-italic">
      This game record had no journal entries.
    </span>
  {:else}
  {#each journalEntries as e, _}
    <JournalEntry text={e.text} snapshot={e.snapshot} />
  {/each}
  {/if}
  {:catch error}
    <h1>
      No journal entries could be retrieved for this game record.
    </h1>
  {/await}
  {/if}
</main>

{#if record !== null}
<Modal bind:this={buildCodeModal} --width="max(60vw, 500px)">
  <div slot="modalHeader">
    Build code
  </div>

  <div slot="modalBody">
    <ClipboardWidget>
      {record.build_code}
    </ClipboardWidget>
  </div>
</Modal>
{/if}
