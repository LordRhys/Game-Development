package net.lordrhystower.gamedev;

import javax.swing.*;
import java.awt.*;

/**
 * Created by hbao506 on 10/20/2014.
 */
public class TextureManager {

  public  static Image loadTexture(String resourceId){
    return new ImageIcon("res/" + resourceId + ".png").getImage();
  }
}
