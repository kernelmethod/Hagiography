<script>
  import { onMount } from "svelte";
  import ColorizedText from "$components/ColorizedText.svelte";
  import GameTileFromString from "$components/GameTileFromString.svelte";
  import Spinner from "$components/Spinner.svelte";
  import DateTime from "$components/DateTime.svelte";

  const endpoint = "/api/records/id";

  let waitingForRecord = true;
  let record = null;
  let recordPromise = null;

  async function fetchRecord() {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');

    await fetch(endpoint + "/" + id)
      .then(response => {
        if (response.status != 200)
          throw new Error("unable to retrieve record");
        return response.json();
      })
      .then(response => {
        record = response;
      })
      .finally(() => {
        waitingForRecord = false;
      });
  }

  onMount(() => { recordPromise = fetchRecord(); });
</script>

<style>
  .headline {
    display: flex;
    align-items: flex-end;
    flex-wrap: wrap;
    margin-bottom: 1rem;
  }

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
  <div class="headline">
    <GameTileFromString --height="calc(6*var(--base-font-size))" spec="{record.tile}" showBackground={false} />
    <span class="character-name">
      <h1>
        <ColorizedText text="{record.character_name}" />
      </h1>
    </span>
  </div>

  <p><b>Game mode:</b> {record.game_mode}</p>
  <p><b>Score:</b> {record.score}</p>
  <p><b>Turns played:</b> {record.turns}</p>
  <p><b>Played on:</b> <DateTime timestamp="{record.created}" /></p>
  {:catch error}
  <h1 class="text-error">{error}</h1>
  {/await}
  {/if}
</main>
