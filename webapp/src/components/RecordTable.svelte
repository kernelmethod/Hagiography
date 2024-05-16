<!-- List of game record stubs, shown in a table -->
<script>
  import { onMount } from "svelte";
  import DateTime from "$components/DateTime.svelte";
  import GameTileFromString from "$components/GameTileFromString.svelte";
  import ColorizedText from "$components/ColorizedText.svelte";
  import Spinner from "$components/Spinner.svelte";

  let waitingForRecords = true;
  let records = null;
  let listRecordsPromise = null;
  const endpoint = "/api/records/list";

  function visitRecord(record) {
    window.location = "/records?id=" + record.id;
  }

  async function listRecords() {
    return await fetch(endpoint)
      .then(response => response.json())
      .then(response => {
        return response.records;
      })
      .catch(err => {
        console.log("Error retrieving records: " + err);
        return [];
      })
      .finally(() => {
        waitingForRecords = false;
      });
  }

  onMount(() => { listRecordsPromise = listRecords(); });
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

  .character-name > span {
    max-width: 400px;
    padding-left: 1rem;
  }
</style>

<div class="flex my-4 justify-center">
  <table class="w-10/12 border-x border-b">
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
            <div class="character-name text-wrap">
              <span class="d-inline-block text-truncate">
                <ColorizedText text="{r.character_name}" />
              </span>
            </div>
          </div>
        </td>
        <td class="hidden lg:table-cell">{r.score}</td>
        <td class="hidden lg:table-cell">{r.turns}</td>
        <td><DateTime timestamp="{r.created}" /></td>
      </tr>
      {/each}
      {/if}
      {/await}
      {/if}
    </tbody>
  </table>
</div>
