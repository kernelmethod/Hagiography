<script>
  export let id;
</script>

<style>
  .btn-link {
    color: var(--qudcolor-y);
  }

  .modal-input {
    color: black;
  }
</style>

<div class="modal fade" id="{id}Toggle" tabindex="-1" aria-labelledby="{id}Label" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <span class="modal-title fs-5 fw-bold" id="{id}Label">
          <slot name="modalHeader" />
        </span>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <slot name="modalBody" />
      </div>
      <div class="modal-footer">
        <slot name="modalFooter" />
      </div>
    </div>
  </div>
</div>


