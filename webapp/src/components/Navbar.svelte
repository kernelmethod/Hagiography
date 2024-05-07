<script>
  import Modal from '$components/Modal.svelte';
  import GameTile from '$components/GameTile.svelte';

  let email = '';
  let password = '';

  let loginForm;
  let signupForm;
  let forgotPasswordForm;

  let loginPromise = null;

  async function attemptLogin() {
    loginForm.classList.add('was-validated');

    if (!loginForm.checkValidity())
      return;

    const data = JSON.stringify({
      email: email,
      password: password,
    });

    const settings = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: data,
    };

    await fetch('/api/auth/login', settings)
      .then(response => {
        if (response.ok)
          return response.json();

        throw new Error("unable to login");
      })
      .then(response => console.log(response))
      .catch(err => console.log(err));
  }

  function sendSignupLink() {
    signupForm.checkValidity();
    signupForm.classList.add('was-validated');
  }

  function sendPasswordResetLink() {
    forgotPasswordForm.checkValidity();
    forgotPasswordForm.classList.add('was-validated');
  }
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
<Modal id="loginModal">
  <span slot="modalHeader">
    Login to Hagiography
  </span>

  <div slot="modalBody">
    <form bind:this={loginForm} class="needs-validation" novalidate>
      <div class="mb-3">
        <label for="email" class="col-form-label">Email:</label>
        <div class="input-group has-validation">
          <input bind:value={email} type="text" class="form-control modal-input" id="email" required>
          <div class="invalid-feedback">
            Please enter your email address
          </div>
        </div>
      </div>
      <div class="mb-3">
        <label for="message-text" class="col-form-label">Password:</label>
        <div class="input-group has-validation">
          <input bind:value={password} type="password" class="form-control modal-input" id="password" required>
          <div class="invalid-feedback">
            Please enter your password
          </div>
        </div>
      </div>
    </form>

    <button class="btn btn-link" data-bs-target="#forgotPasswordModalToggle" data-bs-toggle="modal">
      I forgot my password
    </button>
    <button class="btn btn-link" data-bs-target="#signupModalToggle" data-bs-toggle="modal">
      Create a new account
    </button>
  </div>

  <div slot="modalFooter">
    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
    <button type="button" class="btn btn-primary" on:click={attemptLogin}>Login</button>
  </div>
</Modal>

<!-- Signup modal -->
<Modal id="signupModal">
  <span slot="modalHeader">
    Sign up for Hagiography
  </span>
  <div slot="modalBody">
    <form bind:this={signupForm} class="needs-validation" novalidate>
      <div class="mb-3">
        <label for="email" class="col-form-label">Email:</label>
        <div class="input-group has-validation">
          <input bind:value={email} type="text" class="form-control modal-input" id="email" required>
          <div class="invalid-feedback">
            Please enter your email address
          </div>
        </div>
      </div>
    </form>

    <button class="btn btn-link" data-bs-target="#loginModalToggle" data-bs-toggle="modal">
      Return to login
    </button>
  </div>

  <div slot="modalFooter">
    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
    <button type="button" class="btn btn-primary" on:click={sendSignupLink}>Send signup link</button>
  </div>
</Modal>

<!-- Forgot password modal -->
<Modal id="forgotPasswordModal">
  <span slot="modalHeader">
    Reset password
  </span>

  <div slot="modalBody">
    <form bind:this={forgotPasswordForm} class="needs-validation" novalidate>
      <div class="mb-3">
        <label for="email" class="col-form-label">Email:</label>
        <div class="input-group has-validation">
          <input bind:value={email} type="text" class="form-control modal-input" id="email" required>
          <div class="invalid-feedback">
            Please enter your email address
          </div>
        </div>
      </div>
    </form>

    <button class="btn btn-link" data-bs-target="#loginModalToggle" data-bs-toggle="modal">
      Return to login
    </button>
  </div>

  <div slot="modalFooter">
    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
    <button type="button" class="btn btn-primary" on:click={sendPasswordResetLink}>Send password reset link</button>
  </div>
</Modal>
