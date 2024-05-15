<script>
  let text;
  let copiedPromise = new Promise(r => r());

  async function copyToClipboard() {
    navigator.clipboard
      .writeText(text.innerText)
      .catch(err => {
        console.error(`Error copying to clipboard: ${err}`);
        throw err;
      });

    await new Promise(r => setTimeout(r, 2000));
  }
</script>

<style lang="postcss">
  .clipboard-text {
    background-color: black;
    word-break: break-all;
    padding: 1em;
    margin-top: 1em;
    margin-bottom: 1em;
    color: var(--qudcolor-y);
  }

  .clipboard-button {
    border-bottom: 2px dashed var(--qudcolor-y);
    padding: 0 0 0.5em 0;
    margin: 0 0 0.5em 0;
  }

  .clipboard-button > button {
    text-align: left;
    width: 100%;
  }

  .clipboard-button > button:hover {
    background-color: #1a1919;
  }
</style>

<div class="clipboard-text">
  <div class="clipboard-button">
    <button class="btn" on:click={() => { copiedPromise = copyToClipboard(); }}>
      {#await copiedPromise}
      <i class="bi-clipboard-check"></i> <span class="text-success">Copied!</span>
      {:then}
      <i class="bi-clipboard"></i> Copy to clipboard
      {:catch}
      <i class="bi-clipboard-x"></i> <span class="text-error">There was an error copying to your clipboard</span>
      {/await}
    </button>
  </div>
  <div bind:this={text}>
    <slot />
  </div>
</div>
