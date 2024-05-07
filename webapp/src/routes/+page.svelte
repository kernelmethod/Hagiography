<script>
  import GameTile from "$components/GameTile.svelte";
  import RecordTable from "$components/RecordTable.svelte";
</script>

<div class="text-center" style="margin-bottom: 2rem;">
  <GameTile
    --height="128px"
    tileURL="/Textures/Creatures/sw_biographer_bot.bmp"
    renderString="6"
    colorString="y"
    detailColor="Y" />
  <h2>
    Welcome to <b>Hagiography</b>!
  </h2>
</div>

<p>Live and drink.</p>

<RecordTable />
