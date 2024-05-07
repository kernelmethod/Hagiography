<script>
  import GameTile from "$components/GameTile.svelte";
</script>

<style>
  .nav-background {
    background-color: black;
    width: 100%;
    position: relative;
    margin-bottom: 2em;
  }

  nav {
    background-color: black;
    width: 100%;
    padding: 0;
  }
</style>

<div class="nav-background">
  <div class="container">
    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">
          <div style="display: flex; align-items: center; flex-wrap: wrap;">
            <GameTile
              --height="calc(1.25 * var(--bs-navbar-brand-font-size))"
              tileURL="/Textures/Creatures/sw_biographer_bot.bmp"
              renderString="6"
              colorString="y"
              detailColor="Y" />
            <span class="d-inline-block p-2">
              <b>Hagiography</b>
            </span>
          </div>
        </a>
      </div>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarToggler" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarToggler">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="#">Stats</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Search</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Login</a>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</div>

