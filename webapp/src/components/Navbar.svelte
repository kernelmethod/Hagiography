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
      setTimeout(() => { console.log('closing login modal'); loginModal.hide(); }, 500);
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
      setTimeout(() => { console.log('hiding modal'); logoutModal.hide(); }, 750);
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

<style lang="postcss">
  .nav-background {
    background-color: black;
    width: 100%;
    position: relative;
    margin-bottom: 2em;
  }

  nav {
    width: 100%;
    color: var(--qudcolor-c);
  }

  nav a {
    color: var(--qudcolor-c);
    text-decoration: none;
  }

  .modal-input {
    color: black;
  }

  /* Hide submit inputs */
  input[type=submit] {
    display: none;
  }

  /* Nav item styling */
  .btn-link {
    color: var(--qudcolor-C);
  }
</style>

<div class="nav-background">
  <nav class="flex flex-row container mx-auto py-2">
    <a href="/">
      <div class="flex flex-row items-stretch">
        <HeroIcon --height="64px" />
        <div class="px-2 flex flex-col justify-center items-center">
          <span class="text-3xl font-bold">Hagiography</span>
        </div>
      </div>
    </a>

    <div class="flex-auto"></div>

    {#if $userInfo !== null}
    {#if $userInfo.isLoggedIn()}
    <!-- Options for logged-in users -->
    <div class="flex flex-col justify-center items-center text-xl px-2">
      <a href="/profile">
        <button type="button">
          Profile
        </button>
      </a>
    </div>

    <div class="flex flex-col justify-center items-center text-xl px-2">
      <button type="button" on:click={() => (logoutPromise = attemptLogout())} >
        Logout
      </button>
    </div>
    {:else}
    <!-- Options for logged-out users -->
    <div class="flex flex-col justify-center items-center text-xl px-2">
      <button type="button" on:click={() => loginModal.show()}>
        Login
      </button>
    </div>
    {/if}
    {/if}

    <div class="flex flex-col justify-center items-center text-xl px-2">
      <button type="button" on:click={() => settingsModal.show()}>
        Settings
      </button>
    </div>

  </nav>
</div>

<!-- Login modal -->
<Modal bind:this={loginModal}>
  <span slot="modalHeader">
    Login to Hagiography
  </span>

  <div slot="modalBody">
    <form bind:this={loginForm} on:submit|preventDefault={loginButton} class="needs-validation" novalidate>
      <div class="mb-3">
        <label for="email" class="col-form-label font-bold">Email:</label>
        <div class="input-group has-validation">
          <input bind:value={email} type="text" class="form-control modal-input w-9/12 rounded-sm" id="email" required>
          <div class="invalid-feedback">
            Please enter your email address
          </div>
        </div>
      </div>
      <div class="mb-3">
        <label for="message-text" class="col-form-label font-bold">Password:</label>
        <div class="input-group has-validation">
          <input bind:value={password} type="password" class="form-control modal-input w-9/12 rounded-sm" id="password" required>
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

    <div class="grid grid-flow-col">
      <div>
        <button class="btn-link">I forgot my password</button>
        <button class="btn-link">Create a new account</button>
      </div>
    </div>
  </div>

  <div slot="modalFooter">
    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
    <button type="button" class="btn btn-primary" on:click={loginButton}>Login</button>
  </div>
</Modal>

<!-- Signup modal -->
<Modal>
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
<Modal>
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
<Modal bind:this={logoutModal}>
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
<Modal bind:this={settingsModal}>
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
