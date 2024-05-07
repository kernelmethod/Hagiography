<!-- List of game record stubs, shown in a table -->
<script>
  import { onMount } from "svelte";
  import DateTime from "$components/DateTime.svelte";
  import GameTileFromString from "$components/GameTileFromString.svelte";
  import ColorizedText from "$components/ColorizedText.svelte";
  import Spinner from "$components/Spinner.svelte";

  let records = null;
  const endpoint = "/api/records/list";

  function visitRecord(record) {
    window.location = "/records?id=" + record.id;
  }

  onMount(async function () {
    const response = await fetch(endpoint)
      .then(response => response.json())
      .then(response => {
        records = response.records;
      })
      .catch(err => {
        records = [];
        console.log("Error retrieving records: " + err);
      });
  });
</script>

<style>
  table {
    font-size: calc(0.75 * var(--base-font-size));
  }

  td {
    color: var(--qudcolor-y);
    background: rgba(0, 0, 0, 0);
  }

  .record:hover {
    background-color: var(--table-highlight);
    cursor: pointer;
  }
</style>

<table class="table bg-body-tertiary border border-primary align-middle table-responsive">
  <thead>
    <tr>
      <th scope="col">Game mode</th>
      <th scope="col">Character</th>
      <th scope="col">Score</th>
      <th scope="col">Turns</th>
      <th scope="col">Uploaded</th>
    </tr>
  </thead>
  <tbody>
  {#if records === null || records.length === 0}
    <tr>
      <td style="text-align: center;" colspan="5">
        {#if records === null}
        <!-- Records haven't been retrieved yet -->
        <Spinner>
          Loading game records...
        </Spinner>
        {:else}
        <!-- Records retrieved, none found -->
        No records could be found at this time.
        {/if}
      </td>
    </tr>
  {:else}
  {#each records as r, _}
    <tr on:click={() => visitRecord(r)} class="record">
      <td>{r.game_mode}</td>
      <td>
        <div style="display: flex; align-items: center; flex-wrap: wrap;">
          <GameTileFromString --height="var(--base-font-size)" spec="{r.tile}" />
          <span class="d-inline-block text-truncate" style="max-width: 400px; padding-left: 1rem;">
            <ColorizedText text="{r.character_name}" />
          </span>
        </div>
      </td>
      <td>{r.score}</td>
      <td>{r.turns}</td>
      <td><DateTime spec="{r.created}" /></td>
    </tr>
  {/each}
  {/if}
  </tbody>
</table>
