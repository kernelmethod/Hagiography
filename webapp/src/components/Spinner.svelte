<style>
.loader {
  height: var(--size, 48px);
  width: var(--size, 48px);
  border-radius: 50%;
  display: inline-block;
  position: relative;
  border: 3px solid;
  border-color: var(--qudcolor-b) var(--qudcolor-b) transparent transparent;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}
.loader::after,
.loader::before {
  content: '';
  box-sizing: border-box;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  margin: auto;
  border: 3px solid;
  border-color: transparent transparent var(--qudcolor-y) var(--qudcolor-y);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  box-sizing: border-box;
  animation: rotationBack 0.5s linear infinite;
  transform-origin: center center;
}
.loader::before {
  width: calc(var(--size, 48px) * 2/3);
  height: calc(var(--size, 48px) * 2/3);
  border-color: var(--qudcolor-g) var(--qudcolor-g) transparent transparent;
  animation: rotation 1.5s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
@keyframes rotationBack {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-360deg);
  }
}
</style>

<div class="loader" role="status">
  <span class="visually-hidden">
    <slot />
  </span>
</div>
