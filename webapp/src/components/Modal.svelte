<script>
  export let id;

  let modal;

  export const hide = () => bootstrap.Modal.getInstance(modal).hide();
  export const show = () => (new bootstrap.Modal(modal)).show();
</script>

<style>
  .modal-dialog {
    max-width: var(--width, var(--bs-modal-width));
  }
</style>

<div bind:this={modal} class="modal fade" id="{id}Toggle" tabindex="-1" aria-labelledby="{id}Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      {#if $$slots.modalHeader}
      <div class="modal-header">
        <span class="modal-title fs-5 fw-bold" id="{id}Label">
          <slot name="modalHeader" />
        </span>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      {/if}
      <div class="modal-body">
        <slot name="modalBody" />
      </div>
      {#if $$slots.modalFooter}
      <div class="modal-footer">
        <slot name="modalFooter" />
      </div>
      {/if}
    </div>
  </div>
</div>


