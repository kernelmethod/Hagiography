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
    color: var(--qudcolor-y);
  }

  button {
    text-align: left;
    width: 100%;
  }

  button:hover {
    background-color: #1a1919;
  }
</style>

<div class="clipboard-text p-2 my-2">
  <button class="p-2 rounded-lg" on:click={() => { copiedPromise = copyToClipboard(); }}>
    {#await copiedPromise}
    <span class="text-success">
      <i class="bi-clipboard-check"></i> Copied!
    </span>
    {:then}
    <i class="bi-clipboard"></i> Copy to clipboard
    {:catch}
    <span class="text-error">
      <i class="bi-clipboard-x"></i> There was an error copying to your clipboard
    </span>
    {/await}
  </button>
  <div class="border-t-2 p-2 border-dashed mt-2" bind:this={text}>
    <slot />
  </div>
</div>
