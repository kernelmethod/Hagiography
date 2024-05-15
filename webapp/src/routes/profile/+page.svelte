<script>
  import { onDestroy } from 'svelte';
  import { userInfo, fetcher } from '$js/Auth.jsx';
  import ClipboardWidget from '$components/ClipboardWidget.svelte';
  import Modal from '$components/Modal.svelte';
  import Spinner from '$components/Spinner.svelte';

  let generateApiKeyModal;
  let generateApiKeyPromise = null;

  // Redirect to landing page when the user logs out.
  const unsubscribeUserInfo = userInfo.subscribe((value) => {
    if (value === null)
      return;
    if (!value.isLoggedIn())
      window.location = "/";
  });

  onDestroy(unsubscribeUserInfo);

  async function generateApiKey() {
    generateApiKeyModal.show();

    const settings = {
      method: 'POST'
    };

    return await fetcher('/api/auth/apikeys/generate', settings)
      .then(response => {
        if (response.ok)
          return response.json();

        console.log(response);
        throw new Error('failed to retrieve API key');
      })
      .then(response => {
        return response.token;
      });
  }
</script>

<main>
  {#if $userInfo !== null}
  <h1>
    Profile for <b>{$userInfo.username}</b>
  </h1>

  <button type="button" class="btn btn-primary" on:click={() => generateApiKeyPromise = generateApiKey()}>
    Generate API key
  </button>
  {/if}
</main>

<Modal id="generateApiKeyModal" bind:this={generateApiKeyModal} --width="var(--wide-modal-width)">
  <span slot="modalHeader">
    API key
  </span>

  <div slot="modalBody">
    {#if generateApiKeyPromise != null}
    {#await generateApiKeyPromise}
    <div class="text-center">
      <Spinner>
        Fetching API key...
      </Spinner>
    </div>
    {:then apikey}
    <p>
      Here is your key for uploading your games to Hagiography.
    </p>
    <p class="text-error">
      Do <b>NOT</b> share this key with anyone else!
    </p>
    <ClipboardWidget>
      {apikey}
    </ClipboardWidget>
    <p>
      To use this key:
    </p>
    <ul class="list-disc ml-6">
      <li>Install the Hagiography mod, if you haven't already.</li>
      <li>Start Caves of Qud and go to the options menu.</li>
      <li>Under the "Hagiography" options, click "enter token for Hagiography".</li>
      <li>Copy-and-paste the string above into the dialog that pops up.</li>
    </ul>
    {:catch error}
    <p class="text-error">
      {error}
    </p>
    {/await}
    {/if}
  </div>
</Modal>
