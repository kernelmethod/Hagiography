<script>
  import { parseTileSpec } from "$js/Tile.jsx";
  import GameTile from "$components/GameTile.svelte";

  export let spec;
  export let showBackground = true;

  let tile = parseTileSpec(spec);
</script>

<style>
  div {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    --height2: var(--height, 100%);
  }
</style>

<div>
  <GameTile --height="var(--height2)" tile={tile} showBackground={showBackground} />
</div>
