<script>
  let visible = false;
  let modal;
  const id = crypto.randomUUID();

  export const show = () => (visible = true);
  export const hide = () => modal.close();

  $: if (modal && visible) modal.showModal();
</script>

<style lang="postcss">
  dialog {
    background-color: var(--bg-color);
    color: var(--qudcolor-y);
    border-color: var(--qudcolor-y);
    width: var(--width, 500px);
  }

  dialog[open] {
    animation: zoom 0.3s ease-out;
  }

  dialog::backdrop {
    background-color: rgba(0, 0, 0, 0.7);
  }

  dialog[open]::backdrop {
    animation: fade 0.2s ease-out;
  }

  @keyframes zoom {
    from {
      transform: scale(0.95);
    }

    to {
      transform: scale(1);
    }
  }

  @keyframes fade {
    from {
      opacity: 0;
    }

    to {
      opacity: 1;
    }
  }
</style>

<dialog
  class="mt-32 border-8"
  bind:this={modal}
  id="{id}Toggle"
  aria-labelledby="{id}Label"
  aria-hidden="true"
  on:close={() => (visible = false)}
  on:click|self={() => modal.close()}>

  <div class="modal-content">
    {#if $$slots.modalHeader}
    <div class="border-b-4 border-inherit flex flex-row">
      <span class="text-2xl m-2 font-bold" id="{id}Label">
        <slot name="modalHeader" />
      </span>
      <div class="flex-auto"></div>
      <button type="button" class="px-4" aria-label="Close" on:click={() => modal.close()}>
        <i class="bi-x text-4xl"></i>
      </button>
    </div>
    {/if}
    <div class="p-4">
      <slot name="modalBody" />
    </div>
    {#if $$slots.modalFooter}
    <div class="mt-2 border-t-4 border-inherit p-2">
      <slot name="modalFooter" />
    </div>
    {/if}
  </div>

</dialog>
