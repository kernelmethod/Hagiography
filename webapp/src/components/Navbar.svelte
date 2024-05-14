<script>
  import { onDestroy } from 'svelte';
  import HeroIcon from '$components/HeroIcon.svelte';
  import Modal from '$components/Modal.svelte';
  import Spinner from '$components/Spinner.svelte';

  import { userInfo, fetcher } from '$js/Auth.jsx';
  import { enableTiles } from '$js/Settings.jsx';

  let email = '';
  let password = '';

  let loginForm, loginModal;
  let signupForm;
  let forgotPasswordForm;
  let logoutModal;
  let settingsModal;

  let loginPromise = null;
  let logoutPromise = null;

  let enableTilesCheckbox;

  function loginButton() {
    loginForm.classList.add('was-validated');

    if (!loginForm.checkValidity())
      return;

    loginPromise = attemptLogin();
  }

  async function attemptLogin() {
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

    await fetcher('/api/auth/login', settings)
      .then(response => {
        if (response.ok)
          return response.json();

        throw new Error("unable to login");
      })
      .then(response => {
        userInfo.login(response.username, response.id);
      })
      .catch(err => {
        console.log(err);
        throw err;
      });

    // Sleep for a short period before closing the login modal
    return () => new Promise(resolve => {
      setTimeout(() => { loginModal.hide(); }, 500);
    });
  }

  async function attemptLogout() {
    logoutModal.show();

    const settings = {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    };

    await fetcher('/api/auth/logout', settings)
      .then(response => {
        if (response.ok)
          return response.json();

        throw new Error("logout error");
      })
      .catch(err => {
        console.log(err);
        throw err;
      })
      .finally(() => {
        userInfo.logout();
      });

    return () => new Promise(resolve => {
      setTimeout(() => { logoutModal.hide(); }, 750);
    });
  }

  function sendSignupLink() {
    signupForm.checkValidity();
    signupForm.classList.add('was-validated');
  }

  function sendPasswordResetLink() {
    forgotPasswordForm.checkValidity();
    forgotPasswordForm.classList.add('was-validated');
  }

  const unsubscribe = enableTiles.subscribe((value) => {
    enableTilesCheckbox = value;
  });

  onDestroy(unsubscribe);
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

  .navbar-brand > div {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
  }

  ul {
    align-items: center;
  }

  .modal-input {
    color: black;
  }

  .btn-dark {
    --bs-btn-color: var(--qudcolor-y);
  }

  /* Hide submit inputs */
  input[type=submit] {
    display: none;
  }

  /* Nav item styling */
  .btn-link {
    color: var(--qudcolor-y);
  }

  a.btn {
    padding: 0;
  }

  .nav-item {
    padding: 0 0.25em 0 0.25em;
  }
</style>

<div class="nav-background">
  <div class="container">
    <nav class="navbar navbar-expand-lg">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">
          <div>
            <HeroIcon --height="calc(1.25 * var(--bs-navbar-brand-font-size))" />
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
          {#if $userInfo !== null}
          {#if $userInfo.isLoggedIn()}
          <!-- Options for logged-in users -->
          <li class="nav-item">
            <a href="/profile" class="btn">
              <button type="button" class="btn btn-dark">
                Profile
              </button>
            </a>
          </li>
          <li class="nav-item">
            <button type="button" class="btn btn-dark" on:click={() => logoutPromise = attemptLogout()}>
              Logout
            </button>
          </li>
          {:else}
          <!-- Options for logged-out users -->
          <li class="nav-item">
            <button type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#loginModalToggle">
              Login
            </button>
          </li>
          {/if}
          {/if}
          <li class="nav-item">
            <button type="button" class="btn btn-dark" data-bs-toggle="modal" data-bs-target="#settingsModalToggle">
              Settings
            </button>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</div>

<!-- Login modal -->
<Modal id="loginModal" bind:this={loginModal}>
  <span slot="modalHeader">
    Login to Hagiography
  </span>

  <div slot="modalBody">
    <form bind:this={loginForm} on:submit|preventDefault={loginButton} class="needs-validation" novalidate>
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
      <input type="submit">
    </form>

    {#if loginPromise !== null}
      <div class="text-center">
        {#await loginPromise}
        <Spinner>
          Attempting to login...
        </Spinner>
        {:then exitModalPromise}
          {#await exitModalPromise()}
          <span class="text-success">
            Login successful!
          </span>
          {/await}
        {:catch error}
        <span class="text-error">
          {error}
        </span>
        {/await}
      </div>
    {/if}

    <button class="btn btn-link" data-bs-target="#forgotPasswordModalToggle" data-bs-toggle="modal">
      I forgot my password
    </button>
    <button class="btn btn-link" data-bs-target="#signupModalToggle" data-bs-toggle="modal">
      Create a new account
    </button>
  </div>

  <div slot="modalFooter">
    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
    <button type="button" class="btn btn-primary" on:click={loginButton}>Login</button>
  </div>
</Modal>

<!-- Signup modal -->
<Modal id="signupModal">
  <span slot="modalHeader">
    Sign up for Hagiography
  </span>
  <div slot="modalBody">
    <form bind:this={signupForm} on:submit|preventDefault={sendSignupLink} class="needs-validation" novalidate>
      <div class="mb-3">
        <label for="email" class="col-form-label">Email:</label>
        <div class="input-group has-validation">
          <input bind:value={email} type="text" class="form-control modal-input" id="email" required>
          <div class="invalid-feedback">
            Please enter your email address
          </div>
        </div>
      </div>
      <input type="submit">
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
    <form bind:this={forgotPasswordForm} on:submit|preventDefault={sendPasswordResetLink} class="needs-validation" novalidate>
      <div class="mb-3">
        <label for="email" class="col-form-label">Email:</label>
        <div class="input-group has-validation">
          <input bind:value={email} type="text" class="form-control modal-input" id="email" required>
          <div class="invalid-feedback">
            Please enter your email address
          </div>
        </div>
      </div>
      <input type="submit">
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

<!-- Logout modal -->
<Modal id="logoutModal" bind:this={logoutModal}>
  <span slot="modalHeader">
    Logout
  </span>

  <div slot="modalBody" class="text-center">
    {#if logoutPromise !== null}
    {#await logoutPromise}
    <Spinner>
      Waiting for logout...
    </Spinner>
    {:then exitModalPromise}
      {#await exitModalPromise()}
      <span class="text-success">
        Logout successful!
      </span>
      {/await}
    {:catch error}
    <span class="text-error">
      {error}
    </span>
    {/await}
    {/if}
  </div>
</Modal>

<!-- Settings modal -->
<Modal id="settingsModal" bind:this={settingsModal}>
  <span slot="modalHeader">
    Settings
  </span>

  <div slot="modalBody" class="container form-check">
    <div class="form-check">
      <input type="checkbox" class="form-check-input" id="enableTilesCheckbox"
          bind:checked={enableTilesCheckbox}
          on:change={() => enableTiles.toggle(enableTilesCheckbox)}>
      <label for="enableTilesCheckbox" class="form-check-label">
        Enable tiles
      </label>
    </div>
  </div>
</Modal>
