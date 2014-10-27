package net.lordrhystower.gamedev;

import net.lordrhystower.gamedev.reference.References;

import java.util.Random;

/**
 * Created by hbao506 on 10/22/2014.
 */
public class SimplexNoise {

  SimplexNoiseOctave[] octaves;
  double[] frequencies;
  double[] amplitudes;

  public SimplexNoise(int numberOfOctaves, double persistence){
    Random random = new Random(References.SEED);

    octaves = new SimplexNoiseOctave[numberOfOctaves];
    frequencies = new double[numberOfOctaves];
    amplitudes = new double[numberOfOctaves];

    for (int i = 0; i < numberOfOctaves; i++){
      octaves[i] = new SimplexNoiseOctave(random.nextInt());

      frequencies[i] = Math.pow(2,i);
      amplitudes[i] = Math.pow(persistence,octaves.length-i);
    }
  }
}
