package ws.donmez.burulas;

import android.app.ListActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.GestureDetector;
import android.view.MotionEvent;

public class FlingActivity extends ListActivity implements GestureDetector.OnGestureListener {

    private static final int SWIPE_MIN_DISTANCE = 75;
    private static final int SWIPE_MAX_OFF_PATH = 250;
    private static final int SWIPE_THRESHOLD_VELOCITY = 75;

    private GestureDetector gestureDetector;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        gestureDetector = new GestureDetector(this);
    }

    public void next() {
    }

    public void prev() {
    }

    @Override
    public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX, float velocityY) {
        if (Math.abs(e1.getY() - e2.getY()) > SWIPE_MAX_OFF_PATH)
            return true;

        if (e1.getX() - e2.getX() > SWIPE_MIN_DISTANCE &&
            Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY)
            next();
        else if (e2.getX() - e1.getX() > SWIPE_MIN_DISTANCE
                    && Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
            prev();
        }

        return false;
    }

    @Override
    public void onLongPress(MotionEvent e1) {
    }

    @Override
    public boolean onScroll(MotionEvent e1, MotionEvent e2, float vX, float vY) {
        return true;
    }

    @Override
    public boolean onSingleTapUp(MotionEvent e) {
        return true;
    }

    @Override
    public void onShowPress(MotionEvent e) {
    }

    @Override
    public boolean onDown(MotionEvent e) {
        return true;
    }

    @Override
    public boolean dispatchTouchEvent(MotionEvent event) {
        boolean continueProcessing = gestureDetector.onTouchEvent(event);
        if (continueProcessing)
            super.dispatchTouchEvent(event);
        return false;
    }
}

