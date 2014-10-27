package net.lordrhystower.gamedev;

import java.awt.*;

/**
 * Created by Frank on 10/19/2014.
 */
public class Tile {

  public Material material;
  public Image texture;

  public Tile(Material material){
    this.material = material;
    this.texture = TextureManager.loadTexture(this.material.getRandomResourceId());

  }

}
