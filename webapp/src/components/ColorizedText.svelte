<script>
  import { onMount } from 'svelte';
  import { parseTextColorization } from '$js/Color.jsx';

  export let text;
  export let bold = true;

  let textSpan;
  let renderError = null;

  const colorizedFragments = [];

  try {
    const fragments = parseTextColorization(text);
    for (const fragment of fragments) {
      for (const colorizedText of fragment.getColorizedFragments()) {
        colorizedFragments.push(colorizedText);
      }
    }
  }
  catch (error) {
    renderError = error;
  }
</script>

<style lang="postcss">
  span {
    font-family: var(--console-font-family);
    display: block;
  }

  .render-error {
    font-weight: bold !important;
    color: red !important;
  }
</style>

{#if renderError === null}
<span class:font-bold={bold} bind:this={textSpan}>
  {#each colorizedFragments as fragment, _}
  <span class="{fragment.colorClass} block">
    {fragment.text}
  </span>
  {/each}
</span>
{:else}
<span class="render-error">
  {renderError}
</span>
{/if}
