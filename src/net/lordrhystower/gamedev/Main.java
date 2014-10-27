package net.lordrhystower.gamedev;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

import static net.lordrhystower.gamedev.reference.References.*;


/**
 * Created by Frank on 10/16/2014.
 */
public class Main
{
    public static void main(String[] args)
    {
       // Makes sure the GUI updates correctly
       SwingUtilities.invokeLater(new Runnable() {
           @Override
           public void run() {
               new Main();
           }
       });
    }

    public Main()
    {
        // Game object
        GAME = new Game();
        GAME.screen = GAME.new Screen();
        GAME.start();

        // You can customize the screen size under References
        Toolkit toolkit = Toolkit.getDefaultToolkit();
        if(SCREEN_WIDTH == 0)
            SCREEN_WIDTH = toolkit.getScreenSize().width;
        if(SCREEN_HEIGHT == 0)
            SCREEN_HEIGHT = toolkit.getScreenSize().height;

        // Creates a Window
        JFrame frame = new JFrame(TITLE);
        frame.setSize(SCREEN_WIDTH, SCREEN_HEIGHT);
        frame.setUndecorated(true);  //TODO: If use of custom screen size, set this to false and pack the window
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null); // if you are using custom screen size this makes sure its centered

        // Frame listeners
        frame.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {

            }

            @Override
            public void keyPressed(KeyEvent e) {
                if(!PRESSED_KEYS.contains((Integer)e.getKeyCode()))
                    PRESSED_KEYS.add((Integer)e.getKeyCode());
            }

            @Override
            public void keyReleased(KeyEvent e) {
                PRESSED_KEYS.remove((Integer)e.getKeyCode());
            }
        });
        frame.addMouseListener(new MouseListener() {
            @Override
            public void mouseClicked(MouseEvent e) {

            }

            @Override
            public void mousePressed(MouseEvent e) {

            }

            @Override
            public void mouseReleased(MouseEvent e) {

            }

            @Override
            public void mouseEntered(MouseEvent e) {

            }

            @Override
            public void mouseExited(MouseEvent e) {

            }
        });
        frame.addMouseMotionListener(new MouseMotionListener() {
            @Override
            public void mouseDragged(MouseEvent e) {
                MOUSE_X = e.getX();
                MOUSE_Y = e.getY();
            }

            @Override
            public void mouseMoved(MouseEvent e) {
                MOUSE_X = e.getX();
                MOUSE_Y = e.getY();
            }
        });

        // Custom Icon
        //Custom Cursor

        // Adds the Screen
        frame.add(GAME.screen);

        // Makes the window visible
        frame.setVisible(true);
    }
}
