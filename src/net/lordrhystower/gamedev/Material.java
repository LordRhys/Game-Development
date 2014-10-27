package net.lordrhystower.gamedev;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Created by hbao506 on 10/20/2014.
 */
public class Material {

  public static final Material GRASS = new Material("grass");

  private List<String> resourceIds;

  public Material(String resourceId){
    resourceIds = new ArrayList<String>();
    resourceIds.add(resourceId);
  }

  public String getResourceId(int i){
    return resourceIds.get(i);
  }

  Random random = new Random();
  public String getRandomResourceId(){
    return  resourceIds.get(random.nextInt(resourceIds.size()));
  }


}
