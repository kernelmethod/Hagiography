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

  ul {
    align-items: center;
  }

  .btn-link {
    color: var(--qudcolor-y);
  }

  .modal-input {
    color: black;
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
            <button type="button" class="btn" data-bs-toggle="modal" data-bs-target="#loginModalToggle">
              Login
            </button>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</div>

<!-- Login modal -->
<div class="modal fade" id="loginModalToggle" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <span class="modal-title fs-5 fw-bold" id="exampleModalLabel">Login to Hagiography</span>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form>
          <div class="mb-3">
            <label for="email" class="col-form-label">Email:</label>
            <input type="text" class="form-control modal-input" id="email">
          </div>
          <div class="mb-3">
            <label for="message-text" class="col-form-label">Password:</label>
            <input type="password" class="form-control modal-input" id="password">
          </div>
        </form>

        <button class="btn btn-link" data-bs-target="#forgotPasswordModalToggle" data-bs-toggle="modal">
          I forgot my password
        </button>
        <button class="btn btn-link" data-bs-target="#signupModalToggle" data-bs-toggle="modal">
          Create a new account
        </button>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Login</button>
      </div>
    </div>
  </div>
</div>

<!-- Signup modal -->
<div class="modal fade" id="signupModalToggle" tabindex="-1" aria-labelledby="signupModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <span class="modal-title fs-5 fw-bold" id="exampleModalLabel">Sign up for Hagiography</span>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form>
          <div class="mb-3">
            <label for="email" class="col-form-label">Email:</label>
            <input type="text" class="form-control modal-input" id="email">
          </div>
        </form>

        <button class="btn btn-link" data-bs-target="#loginModalToggle" data-bs-toggle="modal">
          Return to login
        </button>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Send signup link</button>
      </div>
    </div>
  </div>
</div>

<!-- Forgot password modal -->
<div class="modal fade" id="forgotPasswordModalToggle" tabindex="-1" aria-labelledby="forgotPasswordModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <span class="modal-title fs-5 fw-bold" id="exampleModalLabel">Login to Hagiography</span>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <form>
          <div class="mb-3">
            <label for="email" class="col-form-label">Email:</label>
            <input type="text" class="form-control modal-input" id="email">
          </div>
        </form>

        <button class="btn btn-link" data-bs-target="#loginModalToggle" data-bs-toggle="modal">
          Return to login
        </button>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Send password reset link</button>
      </div>
    </div>
  </div>
</div>
