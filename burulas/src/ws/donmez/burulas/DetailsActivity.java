package ws.donmez.burulas;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;

public class DetailsActivity extends FlingActivity {

    private enum DetailView {
        FORWARD_ROUTE,
        BACKWARD_ROUTE,
        HOUR
    };

    private DetailView currentView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        currentView = DetailView.FORWARD_ROUTE;
        switchView(currentView);
    }

    @Override
    public void next() {
        switch (currentView) {
            case FORWARD_ROUTE:
                switchView(DetailView.BACKWARD_ROUTE);
                break;
            case BACKWARD_ROUTE:
                switchView(DetailView.HOUR);
                break;
            default:
                break;
        }
    }

    @Override
    public void prev() {
        switch (currentView) {
            case BACKWARD_ROUTE:
                switchView(DetailView.FORWARD_ROUTE);
            case HOUR:
                switchView(DetailView.BACKWARD_ROUTE);
            default:
                break;
        }
    }

    private void switchView (DetailView view) {
        Log.d("Burulas", "Requested to change the view");
        switch (view) {
            case FORWARD_ROUTE:
                setListAdapter(new ArrayAdapter<String>(this,
                                R.layout.custom_row_layout,
                                this.getForwardRoute()));
                break;
             case BACKWARD_ROUTE:
                setListAdapter(new ArrayAdapter<String>(this,
                                R.layout.custom_row_layout,
                                this.getBackwardRoute()));
                break;
            case HOUR:
                setListAdapter(new ArrayAdapter<String>(this,
                                R.layout.custom_row_layout,
                                this.getHourList()));
                break;

       }

        currentView = view;
    }

    private ArrayList<String> getForwardRoute() {
        return BusViewActivity.currentBus.forward;
    }

    private ArrayList<String> getBackwardRoute() {
        return BusViewActivity.currentBus.backward;
    }

    private ArrayList<String> getHourList() {
        List<String> keys = new ArrayList<String>(BusViewActivity.currentBus.hours.keySet());
        ArrayList<String> hours = new ArrayList<String>();

        for (String key : keys) {
            hours.add(key);
            hours.addAll((ArrayList<String>) BusViewActivity.currentBus.hours.get(key));
        }

        return hours;
    }
}
