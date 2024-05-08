<script>
  import { onMount } from 'svelte';
  import { COLORMAP } from '$js/Color.jsx';
  import { ColorString } from '$js/Tile.jsx';

  let canvas;

  export let tile;
  export let showBackground = true;

  onMount(() => {
    const img = new Image();
    img.src = tile.path;

    const ctx = canvas.getContext('2d');

    const primary = COLORMAP[tile.fgColor()];
    const secondary = COLORMAP[tile.detailColor];
    const bgColorStr = tile.bgColor();

    if (tile.hflip) {
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
    }
    if (tile.vflip) {
      ctx.translate(0, canvas.height);
      ctx.scale(1, -1);
    }

    img.onload = () => {
      // ctx.globalCompositionOperation = 'destination-under';
      ctx.drawImage(img, 0, 0);
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;

      for (let i = 0; i < data.length; i += 4) {
        let weight = (data[i] === 255) ? 1 : 0;

        for (let j = 0; j < 3; j++) {
          // Weighted average of color channels for primary and
          // detail colors.
          const pixelColor = (1 - weight) * primary[j] + weight * secondary[j];
          data[i + j] = pixelColor;
        }
      }

      ctx.putImageData(imageData, 0, 0);

      if (showBackground && bgColorStr in COLORMAP) {
        let color = COLORMAP[bgColorStr];
        color = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
        ctx.globalCompositeOperation = 'destination-over'
        ctx.fillStyle = color;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }
    };
  });
</script>

<style>
  canvas {
    height: var(--height, 100%);
    image-rendering: crisp-edges;
  }
</style>

<canvas bind:this={canvas} width=16 height=24></canvas>
