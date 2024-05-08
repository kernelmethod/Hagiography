<script>
  import { onMount } from 'svelte';
  import { parseTextColorization } from '$js/Color.jsx';

  export let text;
  export let bold = true;

  let textSpan;
  let renderError = null;
  let classes = [];

  if (bold)
    classes.push("fw-bold");

  classes = classes.join(" ");

  onMount(() => {
    try {
      let fragments = parseTextColorization(text);
      for (const fragment of fragments) {
        for (const colorizedText of fragment.getColorizedFragments()) {
          let childSpan = document.createElement('span');
          childSpan.classList.add(colorizedText.colorClass);
          childSpan.innerText = colorizedText.text;
          textSpan.appendChild(childSpan);
        }
      }
    }
    catch (error) {
      renderError = error;
    }
  });
</script>

<style>
  span {
    font-family: var(--console-font-family);
  }

  .render-error {
    font-weight: bold !important;
    color: red !important;
  }
</style>

{#if renderError === null}
<span class="{classes}" bind:this={textSpan}></span>
{:else}
<span class="render-error">
  {renderError}
</span>
{/if}
