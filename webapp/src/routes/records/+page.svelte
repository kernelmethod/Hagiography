<script>
  import { onMount } from "svelte";
  import ColorizedText from "$components/ColorizedText.svelte";
  import GameTileFromString from "$components/GameTileFromString.svelte";
  import Spinner from "$components/Spinner.svelte";
  import DateTime from "$components/DateTime.svelte";

  const endpoint = "/api/records/id";

  let record = null;
  let error = null;

  onMount(async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');

    const response = await fetch(endpoint + "/" + id)
      .then(response => response.json())
      .then(response => {
        record = response;
      })
      .catch(err => {
        error = err;
      });
  });
</script>

<style>
  .headline {
    display: flex;
    align-items: flex-end;
    flex-wrap: wrap;
    margin-bottom: 1rem;
  }

  p {
    margin: 0;
  }
</style>

{#if record === null && error === null}
<div class="text-center">
  <Spinner --size="128px">
    Loading character data...
  </Spinner>
</div>
{:else if error !== null}
<h1 class="text-error">Error</h1>
{:else}
<div class="headline">
  <GameTileFromString --height="calc(6*var(--base-font-size))" spec="{record.tile}" />
  <span style="display: inline-block; padding-left: 1rem;">
    <h1>
      <ColorizedText text="{record.character_name}" />
    </h1>
  </span>
</div>

<p><b>Game mode:</b> {record.game_mode}</p>
<p><b>Score:</b> {record.score}</p>
<p><b>Turns played:</b> {record.turns}</p>
<p><b>Played on:</b> <DateTime spec="{record.created}" /></p>

{/if}
