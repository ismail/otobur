package ws.donmez.burulas;

import java.util.ArrayList;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;

public class BackwardStopsActivity extends FlingActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setListAdapter(new ArrayAdapter<String>(this,
                                        android.R.layout.simple_list_item_1,
                                        this.getBackwardRoute()));
    }

    @Override
    public void prev() {
        Intent intent = new Intent(this, ForwardStopsActivity.class);
        startActivity(intent);
        finish();
    }

    private ArrayList<String> getBackwardRoute() {
        return BusViewActivity.currentBus.backward;
    }
}

