<!-- List of game record stubs, shown in a table -->
<script>
  import { onMount } from "svelte";
  import DateTime from "$components/DateTime.svelte";
  import GameTileFromString from "$components/GameTileFromString.svelte";
  import ColorizedText from "$components/ColorizedText.svelte";
  import Spinner from "$components/Spinner.svelte";

  let currentIndex = 0;
  let count = 0;
  const numRetrieved = 10;

  let waitingForRecords = true;
  let records = null;
  let listRecordsPromise = null;

  function visitRecord(record) {
    window.location = "/records?id=" + record.id;
  }

  function fetchRecords(startIndex) {
    if (startIndex < 0)
      return;

    listRecordsPromise = listRecords(startIndex);
    currentIndex = startIndex;
  }

  async function listRecords() {
    const endpoint = `/api/records/list?start=${currentIndex}&end=${currentIndex+numRetrieved}`;
    return await fetch(endpoint)
      .then(response => response.json())
      .then(response => {
        count = response.count || 0;
        return response.records;
      })
      .catch(err => {
        console.error("Error retrieving records: " + err);
        return [];
      })
      .finally(() => {
        waitingForRecords = false;
      });
  }

  onMount(() => { fetchRecords(0); });
</script>

<style lang="postcss">
  thead > tr {
    background-color: white;
    color: black;
  }

  th, td {
    padding-left: 1em;
  }

  td {
    color: var(--qudcolor-y);
  }

  tr {
    background: var(--bg-color);
  }

  .record:hover {
    background: var(--highlight-color);
    cursor: pointer;
  }

  .character-name {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
  }

  button:disabled {
    opacity: 0.5;
  }

  button:disabled:hover {
    background-color: inherit;
  }
</style>

<div class="flex flex-row my-4 justify-center">
  <div class="w-full px-2 lg:w-10/12">
    <table class="border-x border-b w-full">
      <thead class="text-left">
        <tr>
          <th scope="col">Game mode</th>
          <th scope="col">Character</th>
          <th class="hidden lg:table-cell" scope="col">Score</th>
          <th class="hidden lg:table-cell" scope="col">Turns</th>
          <th scope="col">Uploaded</th>
        </tr>
      </thead>
      <tbody class="text-left">
        {#if waitingForRecords}
        <!-- Records haven't been retrieved yet -->
        <tr>
          <td class="text-center" colspan="5">
            <Spinner>
              Loading game records...
            </Spinner>
          </td>
        </tr>
        {/if}
        {#if listRecordsPromise !== null}
        {#await listRecordsPromise then records}
        {#if records.length === 0}
        <tr>
          <td class="multicol-text" colspan="5">
            No records could be found at this time.
          </td>
        </tr>
        {:else}
        {#each records as r, _}
        <tr on:click={() => visitRecord(r)} class="record">
          <td>{r.game_mode}</td>
          <td>
            <div class="flex flex-row">
              <div>
                <GameTileFromString --height="var(--base-font-size)" spec="{r.tile}" showBackground={false} />
              </div>
              <div class="character-name text-wrap mw-96 pl-2">
                <span class="d-inline-block text-truncate">
                  <ColorizedText text="{r.character_name}" />
                </span>
              </div>
            </div>
          </td>
          <td class="hidden lg:table-cell">{r.score}</td>
          <td class="hidden lg:table-cell">{r.turns}</td>
          <td><DateTime showDelta={true} timestamp="{r.created}" /></td>
        </tr>
        {/each}
        {/if}
        {/await}
        {/if}
      </tbody>
    </table>

    <div class="flex flex-row mt-2 px-4">
      <button type="button" class="hover:bg-emerald-900 rounded-md p-2 w-32"
        disabled={currentIndex < numRetrieved}
        on:click={() => null}>
        <i class="bi-arrow-left-square-fill"></i> Previous
      </button>
      <div class="flex-auto"></div>
      <button type="button" class="hover:bg-emerald-900 rounded-md p-2 w-32"
        disabled={currentIndex + numRetrieved >= count}
        on:click={() => null}>
        Next <i class="bi-arrow-right-square-fill"></i>
      </button>
    </div>
  </div>
</div>
