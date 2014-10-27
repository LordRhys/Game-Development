package net.lordrhystower.gamedev.reference;

import net.lordrhystower.gamedev.Game;
import net.lordrhystower.gamedev.GameThread;
import net.lordrhystower.gamedev.Map;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Frank on 10/18/2014.
 */
public class References {

    // MAIN
        public static final String TITLE = "GAME DEVELOPMENT - by ScratchForFun";
        public static int SCREEN_WIDTH;
        public static int SCREEN_HEIGHT;

    // SCREEN
        public static int PIXEL_SIZE = 3; // TODO: Change this to scale!
        public static int TILE_SIZE = 16;

    // GAME THREAD
        public static int UPDATES_PER_SECOND = 50;
        public static int FRAMES_PER_SECOND  = 100;
        public static long MAX_FRAMESKIP = 5;

    // GAME
        public static Game GAME;
        public static int SEED;

    // LISTENER
        public static List<Integer> PRESSED_KEYS = new ArrayList<Integer>();
        public static int MOUSE_X;
        public static int MOUSE_Y;

    // CHUNK
        public static final int TILE_AMOUNT_X = 16;
        public static final int TILE_AMOUNT_Y = 16;
        public static final int CHUNK_AMOUNT_X = 5;
        public static final int CHUNK_AMOUNT_Y = 5;
}
