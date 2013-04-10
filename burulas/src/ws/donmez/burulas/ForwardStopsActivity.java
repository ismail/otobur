package ws.donmez.burulas;

import java.util.ArrayList;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;

public class ForwardStopsActivity extends FlingActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setListAdapter(new ArrayAdapter<String>(this,
                                        android.R.layout.simple_list_item_1,
                                        this.getForwardRoute()));
    }

    @Override
    public void next() {
        ArrayList<String> backwardStops = getIntent().getStringArrayListExtra("BackwardStops");
        Intent intent = new Intent(this, BackwardStopsActivity.class);
        intent.putExtra("BackwardStops", backwardStops);
        startActivity(intent);
    }

    private ArrayList<String> getForwardRoute() {
        Intent intent = getIntent();
        return intent.getStringArrayListExtra("ForwardStops");
    }
}

