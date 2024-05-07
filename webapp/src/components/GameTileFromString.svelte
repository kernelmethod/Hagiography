<script>
  import { parseTileSpec } from "$js/Tile.jsx";
  import GameTile from "$components/GameTile.svelte";

  export let spec;

  let tile = parseTileSpec(spec);
  let texturesURI = new URL("Textures/", document.baseURI);
  let url = new URL(tile.path, texturesURI);
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
  <GameTile
    --height="var(--height2)"
    tileURL="{url}"
    renderString="{tile.renderString}"
    colorString="{tile.colorString}"
    detailColor="{tile.detailColor}"
    tileColor="{tile.tileColor}"
    hflip="{tile.hflip}"
    vflip="{tile.vflip}" />
</div>
